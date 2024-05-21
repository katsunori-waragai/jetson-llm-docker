import argparse
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import inspect

import numpy as np
import cv2
import json
import torch
from PIL import Image

sys.path.append(os.path.join(os.getcwd(), "GroundingDINO"))
sys.path.append(os.path.join(os.getcwd(), "segment_anything"))


# Grounding DINO
import GroundingDINO.groundingdino.datasets.transforms as T
from GroundingDINO.groundingdino.models import build_model
from GroundingDINO.groundingdino.util.slconfig import SLConfig
from GroundingDINO.groundingdino.util.utils import clean_state_dict, get_phrases_from_posmap


# segment anything
from segment_anything import (
    sam_model_registry,
    sam_hq_model_registry,
    SamPredictor
)
import cv2
import numpy as np
import matplotlib.pyplot as plt

COLOR_MAP = {
    0: [0, 0, 0],       # 黒
    1: [0, 255, 0],     # 緑
    2: [0, 0, 255],     # 青
    3: [255, 0, 0],     # 赤
    4: [255, 255, 0],   # 黄色
    5: [255, 0, 255],   # マゼンタ
    6: [0, 255, 255],   # シアン
    7: [128, 128, 128], # グレー
    8: [128, 0, 0],     # マルーン
    9: [128, 128, 0],   # オリーブ
    10: [0, 128, 0],  # ダークグリーン
    11: [0, 128, 128],  # ティール
    12: [0, 0, 128],  # ネイビー
    13: [255, 165, 0],  # オレンジ
    14: [255, 215, 0],  # ゴールド
    15: [173, 216, 230],  # ライトブルー
    16: [75, 0, 130],  # インディゴ
    17: [240, 128, 128],  # ライトコーラル
    18: [244, 164, 96],  # サドルブラウン
    19: [60, 179, 113]  # ミディアムシーブルー
}


def to_json(label_list: List[str], box_list: List, background_value: int=0) -> Dict:
    value = background_value
    json_data = [{
        'value': value,
        'label': 'background'
    }]
    for label, box in zip(label_list, box_list):
        value += 1
        name, logit = label.split('(')
        logit = logit[:-1]  # the last is ')'
        json_data.append({
            'value': value,
            'label': name,
            'logit': float(logit),
            'box': box.numpy().tolist(),
        })
    return json_data


def colorize(segmentation_result: np.ndarray) -> np.ndarray:
    height, width = segmentation_result.shape
    color_image = np.zeros((height, width, 3), dtype=np.uint8)
    num_colors = len(COLOR_MAP)
    maxint = int(np.max(segmentation_result.flatten()))
    for i in range(maxint):
        color_image[segmentation_result == i] = COLOR_MAP[i % num_colors]
    return color_image

def pil2cv(image: Image) -> np.ndarray:
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image: np.ndarray) -> Image:
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def load_model(model_config_path, model_checkpoint_path, device):
    args = SLConfig.fromfile(model_config_path)
    args.device = device
    model = build_model(args)
    checkpoint = torch.load(model_checkpoint_path, map_location="cpu")
    load_res = model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    print(load_res)
    _ = model.eval()
    return model


def get_grounding_output(model, torch_image, caption, box_threshold, text_threshold, with_logits=True, device="cpu"):
    caption = caption.lower()
    caption = caption.strip()
    if not caption.endswith("."):
        caption = caption + "."
    model = model.to(device)
    torch_image = torch_image.to(device)
    with torch.no_grad():
        outputs = model(torch_image[None], captions=[caption])
    logits = outputs["pred_logits"].cpu().sigmoid()[0]  # (nq, 256)
    boxes = outputs["pred_boxes"].cpu()[0]  # (nq, 4)
    logits.shape[0]

    # filter output
    logits_filt = logits.clone()
    boxes_filt = boxes.clone()
    filt_mask = logits_filt.max(dim=1)[0] > box_threshold
    logits_filt = logits_filt[filt_mask]  # num_filt, 256
    boxes_filt = boxes_filt[filt_mask]  # num_filt, 4
    logits_filt.shape[0]

    # get phrase
    tokenlizer = model.tokenizer
    tokenized = tokenlizer(caption)
    # build pred
    pred_phrases = []
    for logit, box in zip(logits_filt, boxes_filt):
        pred_phrase = get_phrases_from_posmap(logit > text_threshold, tokenized, tokenlizer)
        if with_logits:
            pred_phrases.append(pred_phrase + f"({str(logit.max().item())[:4]})")
        else:
            pred_phrases.append(pred_phrase)

    return boxes_filt, pred_phrases


def gen_mask_img(mask_list: torch.Tensor, background_value=0) -> torch.Tensor:
    print(f"{type(mask_list)=}")
    mask_img = torch.zeros(mask_list.shape[-2:])
    print(f"{type(mask_img)=}")
    for idx, mask in enumerate(mask_list):
        mask_img[mask.cpu().numpy()[0] == True] = background_value + idx + 1
    return mask_img

def save_mask_data_jpg(output_mask_jpg: Path, mask_list: torch.Tensor, box_list: List, label_list: List[str]):  # save json file

    mask_img = gen_mask_img(mask_list)
    colorized = colorize(mask_img.numpy())
    cv2.imwrite(str(output_mask_jpg), colorized)
    mask_json = output_mask_jpg.with_suffix(".json")
    with mask_json.open("wt") as f:
        json.dump(to_json(label_list, box_list), f)
    return colorized, mask_img.numpy()


def overlaid_image(boxes_filt: List, pred_phrases: List[str], cvimage: np.ndarray, colorized: np.ndarray) -> np.ndarray:
    assert colorized.shape[2] == 3
    alpha = 0.5
    print(f"{colorized.shape=}")
    assert colorized.shape[2] == 3
    blend_image = np.array(alpha * colorized + (1 - alpha) * cvimage, dtype=np.uint8)
    for box, label in zip(boxes_filt, pred_phrases):
        print(f"{box=} {label=}")
        x1, y1, x2, y2 = [int(a) for a in box]
        cv2.rectangle(blend_image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=3)
        cv2.putText(blend_image, label, (x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(255, 0, 255),
                    thickness=2, )
    return blend_image


def modify_boxes_filter(boxes_filt, W: int, H: int):
    for i in range(boxes_filt.size(0)):
        boxes_filt[i] = boxes_filt[i] * torch.Tensor([W, H, W, H])
        boxes_filt[i][:2] -= boxes_filt[i][2:] / 2
        boxes_filt[i][2:] += boxes_filt[i][:2]

    boxes_filt = boxes_filt.cpu()
    return boxes_filt


@dataclass
class GroundedSAMPredictor:
    # GroundingDino のPredictor
    # SAMのPredictor

    def __post_init__(self):
        # 各modelの設定をする。
        self.model = load_model(config_file, grounded_checkpoint, device=device)
        # initialize SAM
        sam_ckp = sam_hq_checkpoint if use_sam_hq else sam_checkpoint
        self.predictor = SamPredictor(sam_model_registry[sam_version](checkpoint=sam_ckp).to(device))

    def infer_file(self, image_path):
        pass

    def save(self):
        pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Grounded-Segment-Anything Demo", add_help=True)
    parser.add_argument("--config", type=str, required=True, help="path to config file")
    parser.add_argument(
        "--grounded_checkpoint", type=str, required=True, help="path to checkpoint file"
    )
    parser.add_argument(
        "--sam_version", type=str, default="vit_h", required=False, help="SAM ViT version: vit_b / vit_l / vit_h"
    )
    parser.add_argument(
        "--sam_checkpoint", type=str, required=False, help="path to sam checkpoint file"
    )
    parser.add_argument(
        "--sam_hq_checkpoint", type=str, default=None, help="path to sam-hq checkpoint file"
    )
    parser.add_argument(
        "--use_sam_hq", action="store_true", help="using sam-hq for prediction"
    )
    parser.add_argument("--image_dir", type=str, required=True, help="path to image file")
    parser.add_argument("--text_prompt", type=str, required=True, help="text prompt")
    parser.add_argument(
        "--output_dir", "-o", type=str, default="outputs", required=True, help="output directory"
    )

    parser.add_argument("--box_threshold", type=float, default=0.3, help="box threshold")
    parser.add_argument("--text_threshold", type=float, default=0.25, help="text threshold")

    parser.add_argument("--device", type=str, default="cpu", help="running on cpu only!, default=False")
    args = parser.parse_args()

    # cfg
    config_file = args.config  # change the path of the model config file
    grounded_checkpoint = args.grounded_checkpoint  # change the path of the model
    sam_version = args.sam_version
    sam_checkpoint = args.sam_checkpoint
    sam_hq_checkpoint = args.sam_hq_checkpoint
    use_sam_hq = args.use_sam_hq
    image_dir = Path(args.image_dir)
    text_prompt = args.text_prompt
    output_dir = Path(args.output_dir)
    box_threshold = args.box_threshold
    text_threshold = args.text_threshold
    device = args.device

    output_dir.mkdir(exist_ok=True)

    model = load_model(config_file, grounded_checkpoint, device=device)
    # initialize SAM
    sam_ckp = sam_hq_checkpoint if use_sam_hq else sam_checkpoint
    predictor = SamPredictor(sam_model_registry[sam_version](checkpoint=sam_ckp).to(device))

    image_path_list = list(Path(image_dir).glob("*.jpg"))
    for p in image_path_list:
        print(p)

    for image_path in sorted(image_path_list):
        image_pil = Image.open(image_path).convert("RGB")  # load image

        transform = T.Compose(
            [
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        torch_image, _ = transform(image_pil, None)  # 3, h, w
        W, H = image_pil.size[:2]
        image_path_stem = image_path.stem.replace(" ", "_")
        image_pil.save(output_dir / f"{image_path_stem}_raw.jpg")

        # run grounding dino model
        t0 = cv2.getTickCount()
        boxes_filt, pred_phrases = get_grounding_output(
            model, torch_image, text_prompt, box_threshold, text_threshold, device=device
        )
        boxes_filt = modify_boxes_filter(boxes_filt, W, H)
        t1 = cv2.getTickCount()
        used_time = {}
        used_time["grounding"] = (t1 - t0) / cv2.getTickFrequency()
        cvimage = pil2cv(image_pil)

        t2 = cv2.getTickCount()
        if pred_phrases:
            predictor.set_image(cvimage)
            transformed_boxes = predictor.transform.apply_boxes_torch(boxes_filt, cvimage.shape[:2]).to(device)
            masks, _, _ = predictor.predict_torch(
                point_coords = None,
                point_labels = None,
                boxes = transformed_boxes.to(device),
                multimask_output = False,
            )
        else:
            C = len(pred_phrases)
            masks = torch.from_numpy(np.full((C, H, W), False, dtype=np.bool))
        t3 = cv2.getTickCount()
        used_time["sam"] = (t3 - t2) / cv2.getTickFrequency()

        t6 = cv2.getTickCount()
        colorized, mask_image = save_mask_data_jpg(output_dir / f"{image_path_stem}_mask.jpg", masks, boxes_filt, pred_phrases)
        t7 = cv2.getTickCount()
        used_time["save_mask"] = (t7 - t6) / cv2.getTickFrequency()

        t10 = cv2.getTickCount()
        blend_image = overlaid_image(boxes_filt, pred_phrases, cvimage, colorized)
        cv2.imwrite(str(output_dir / f"{image_path_stem}_sam.jpg"), blend_image)
        t11 = cv2.getTickCount()
        used_time["save_sam"] = (t11 - t10) / cv2.getTickFrequency()

        print(f"{used_time=}")
        cv2.imshow("output", blend_image)
        key = cv2.waitKey(10)
