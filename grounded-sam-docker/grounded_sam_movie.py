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
from grounded_sam_demo_my import *

sys.path.append(os.path.join(os.getcwd(), "GroundingDINO"))
sys.path.append(os.path.join(os.getcwd(), "segment_anything"))

"""
まず namespace の問題の解決。
次に、動画入力を受け付けるように改変する。
"""

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

    transform = T.Compose(
        [
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    counter = 0
    while True:
        r, cvimg = cap.read()
        if cvimg is None:
            continue

        counter += 1
        [h, w] = cvimg.shape[:2]
        cvimg = cvimg[:, : w //2,  :]
        image_pil = cv2pil(cvimg)
        image, _ = transform(image_pil, None)  # 3, h, w


        W, H = image_pil.size[:2]
        filename_stem = f"captured_{counter:04d}"
        image_pil.save(output_dir / f"{filename_stem}_raw.jpg")

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

        save_output_jpg(output_dir / f"{filename_stem}_sam.jpg", masks, boxes_filt, pred_phrases, cvimage)
        save_mask_data_jpg(output_dir / f"{filename_stem}_mask.jpg", masks, boxes_filt, pred_phrases)
        print(f"{used_time=}")
        output_img = cv2.imread(str(output_dir / f"{filename_stem}_sam.jpg"))
        cv2.imshow("output", output_img)
        key = cv2.waitKey(10)
