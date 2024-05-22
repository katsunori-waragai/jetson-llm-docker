import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict
import json

import numpy as np
import cv2
from gsam import GroundedSAMPredictor, colorize, overlaid_image, gen_mask_img, to_json


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Grounded-Segment-Anything Demo", add_help=True)
    parser.add_argument(
        "--use_sam_hq", action="store_true", help="using sam-hq for prediction"
    )
    parser.add_argument("--text_prompt", type=str, required=True, help="text prompt")
    parser.add_argument(
        "--output_dir", "-o", type=str, default="outputs", required=True, help="output directory"
    )

    parser.add_argument("--box_threshold", type=float, default=0.3, help="box threshold")
    parser.add_argument("--text_threshold", type=float, default=0.25, help="text threshold")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    output_dir.mkdir(exist_ok=True)

    gsam_predictor = GroundedSAMPredictor(text_prompt=args.text_prompt,
                                          text_threshold=args.text_threshold,
                                          box_threshold=args.box_threshold,
                                          use_sam_hq=args.use_sam_hq
                                          )
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    counter = 0
    while True:
        r, cvimage = cap.read()
        if cvimage is None:
            continue

        counter += 1
        [h, w] = cvimage.shape[:2]
        cvimage = cvimage[:, : w //2,  :]

        gsam_predictor.infer_all(cvimage)
        filename_stem = f"captured_{counter:04d}"
        cv2.imwrite(str(output_dir / f"{filename_stem}_raw.jpg"), cvimage)

        # run grounding dino model
        used_time = gsam_predictor.used.copy()

        masks = gsam_predictor.masks

        t6 = cv2.getTickCount()
        colorized = colorize(gen_mask_img(masks).numpy())
        output_mask_jpg = output_dir / f"{filename_stem}_mask.jpg"
        cv2.imwrite(str(output_mask_jpg), colorized)
        mask_json = output_mask_jpg.with_suffix(".json")
        pred_phrases = gsam_predictor.pred_phrases
        boxes_filt = gsam_predictor.boxes_filt
        with mask_json.open("wt") as f:
            json.dump(to_json(pred_phrases, boxes_filt), f)
        t7 = cv2.getTickCount()
        used_time["save_mask"] = (t7 - t6) / cv2.getTickFrequency()

        t10 = cv2.getTickCount()
        blend_image = overlaid_image(boxes_filt, pred_phrases, cvimage, colorized)
        cv2.imwrite(str(output_dir / f"{filename_stem}_sam.jpg"), blend_image)
        t11 = cv2.getTickCount()
        used_time["save_sam"] = (t11 - t10) / cv2.getTickFrequency()

        print(f"{used_time=}")
        cv2.imshow("output", blend_image)
        key = cv2.waitKey(10)
        if key == ord("q"):
            break
