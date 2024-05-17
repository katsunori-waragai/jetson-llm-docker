import argparse
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

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


def load_image(image_path: Path):
    # load image
    image_pil = Image.open(image_path).convert("RGB")  # load image

    transform = T.Compose(
        [
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image, _ = transform(image_pil, None)  # 3, h, w
    return image_pil, image


def load_model(model_config_path, model_checkpoint_path, device):
    args = SLConfig.fromfile(model_config_path)
    args.device = device
    model = build_model(args)
    checkpoint = torch.load(model_checkpoint_path, map_location="cpu")
    load_res = model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    print(load_res)
    _ = model.eval()
    return model


def get_grounding_output(model, image, caption, box_threshold, text_threshold, with_logits=True, device="cpu"):
    caption = caption.lower()
    caption = caption.strip()
    if not caption.endswith("."):
        caption = caption + "."
    model = model.to(device)
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image[None], captions=[caption])
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

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax, label):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))
    ax.text(x0, y0, label)


def save_mask_data_jpg(output_mask_jpg: Path, mask_list, box_list: List, label_list: List):  # save json file
    value = 0  # 0 for background
    mask_json = output_mask_jpg.with_suffix(".json")

    mask_img = torch.zeros(mask_list.shape[-2:])
    for idx, mask in enumerate(mask_list):
        mask_img[mask.cpu().numpy()[0] == True] = value + idx + 1
    plt.figure(figsize=(10, 10))
    plt.imshow(mask_img.numpy())
    plt.axis('off')
    plt.savefig(output_mask_jpg, bbox_inches="tight", dpi=300, pad_inches=0.0)

    json_data = [{
        'value': value,
        'label': 'background'
    }]
    for label, box in zip(label_list, box_list):
        value += 1
        name, logit = label.split('(')
        logit = logit[:-1] # the last is ')'
        json_data.append({
            'value': value,
            'label': name,
            'logit': float(logit),
            'box': box.numpy().tolist(),
        })
    with mask_json.open("wt") as f:
        json.dump(json_data, f)

def save_output_jpg(output_jpg: Path, masks: List, boxes_filt: List, pred_phrases: List[str], image: np.ndarray):
    """
    save overlay image

    Note: saved image size is not equal to original size.
    """
    output_jpg.parent.mkdir(exist_ok=True, parents=True)
    bgrimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(bgrimage)
    for mask in masks:
        show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)
    for box, label in zip(boxes_filt, pred_phrases):
        show_box(box.numpy(), plt.gca(), label)

    plt.axis('off')
    plt.savefig(
        output_jpg,
        bbox_inches="tight", dpi=300, pad_inches=0.0
    )

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
        image_pil, image = load_image(image_path)
        image_pil.save(output_dir / "raw_image.jpg")

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

    # make dir
    output_dir.mkdir(exist_ok=True)
    # load model
    model = load_model(config_file, grounded_checkpoint, device=device)
    # initialize SAM
    sam_ckp = sam_hq_checkpoint if use_sam_hq else sam_checkpoint
    predictor = SamPredictor(sam_model_registry[sam_version](checkpoint=sam_ckp).to(device))

    for image_path in Path(image_dir).glob("demo*.jpg"):
        # load image
        image_pil, image = load_image(image_path)
        W, H = image_pil.size[:2]
        image_path_stem = image_path.stem.replace(" ", "_")
        # visualize raw image
        image_pil.save(output_dir / f"{image_path_stem}_raw.jpg")

        # run grounding dino model
        t0 = cv2.getTickCount()
        boxes_filt, pred_phrases = get_grounding_output(
            model, image, text_prompt, box_threshold, text_threshold, device=device
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

        save_output_jpg(output_dir / f"{image_path_stem}_sam.jpg", masks, boxes_filt, pred_phrases, cvimage)
        save_mask_data_jpg(output_dir / f"{image_path_stem}_mask.jpg", masks, boxes_filt, pred_phrases)
        print(f"{used_time=}")
        output_img = cv2.imread(str(output_dir / f"{image_path_stem}_sam.jpg"))
        cv2.imshow("output", output_img)
        key = cv2.waitKey(-1)
