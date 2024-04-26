# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt
from nanosam.utils.trt_pose import PoseDetector, pose_to_sam_points
from nanosam.utils.predictor import Predictor

import cvpil

PROJECT_ROOT = Path(__name__).resolve().parent


def predict_and_show(pose, fg_points, bg_points):
    """
    index: 0 to N-1
    pose: detection by pose_model
    fg_points: keys for foreground points
    bg_points: keys for background points
    """
    global sam_predictor
    points, point_labels = pose_to_sam_points(pose, fg_points, bg_points)
    mask, _, _ = sam_predictor.predict(points, point_labels)
    return mask[0, 0].detach().cpu()


def paste(mask0, cvimg: np.ndarray, color: Tuple) -> np.ndarray:
    """
    mask0 == True の領域で、cvimg をcolorで置き換える。
    :param mask0:
    :param cvimg:
    :param color:
    :return:
    """
    assert len(color) == 3
    mask0d = (mask0 > 0).numpy()
    h, w = mask0d.shape[:2]
    merged = np.zeros((h, w, 3), dtype=np.bool_)
    for i in range(3):
        merged[:, :, i] = mask0d
    return np.where(merged, color, cvimg)


def process_frame(cvimg: np.ndarray) -> np.ndarray:
    image = cvpil.cv2pil(cvimg)
    t0 = cv2.getTickCount()
    detections = pose_model.predict(image)
    if len(detections) == 0:
        t1 = cv2.getTickCount()
        used = (t1 - t0) / cv2.getTickFrequency()
        return cvimg
    pose = detections[0]
    sam_predictor.set_image(image)
    N = 4
    mask0 = predict_and_show(
        pose,
        ["left_shoulder", "right_shoulder"],
        ["nose", "left_knee", "right_knee", "left_hip", "right_hip"],
    )
    mask1 = predict_and_show(
        pose,
        ["left_eye", "right_eye", "nose", "left_ear", "right_ear"],
        ["left_shoulder", "right_shoulder", "neck", "left_wrist", "right_wrist"],
    )
    mask2 = predict_and_show(
        pose,
        ["left_hip", "right_hip"],
        ["left_shoulder", "right_shoulder"],
    )
    mask3 = predict_and_show(
        pose,
        ["nose", "left_wrist", "right_wrist", "left_ankle", "right_ankle"],
        ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
    )
    t1 = cv2.getTickCount()
    used = (t1 - t0) / cv2.getTickFrequency()

    cvimg = cvpil.pil2cv(image)
    pasted_cvimg = cvimg.copy()
    pasted_cvimg = paste(mask0, pasted_cvimg, (255, 0, 0))
    pasted_cvimg = paste(mask1, pasted_cvimg, (0, 255, 0))
    pasted_cvimg = paste(mask2, pasted_cvimg, (0, 0, 255))
    pasted_cvimg = paste(mask3, pasted_cvimg, (128, 128, 0))
    pasted_cvimg = pasted_cvimg.astype(np.uint8)
    print(f"{used=:3f} [s]")
    cv2.putText(pasted_cvimg, f"{used:3f} [s]", (30, 30), cv2.FONT_HERSHEY_PLAIN, 2.0,
               (0, 255, 0), 2, cv2.LINE_AA)
    return pasted_cvimg


if __name__ == "__main__":
    import argparse

    DEFAULT_IMAGE = PROJECT_ROOT / "assets/john_1.jpg"
    POSE_MODEL = PROJECT_ROOT / "data/densenet121_baseline_att_256x256_B_epoch_160.pth"
    POSE_JSON = PROJECT_ROOT / "assets/human_pose.json"
    RESNET_ENGINE = PROJECT_ROOT / "data/resnet18_image_encoder.engine"
    SAM_ENGINE = PROJECT_ROOT / "data/mobile_sam_mask_decoder.engine"
    DST_DIR = PROJECT_ROOT / "data"

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default=str(DEFAULT_IMAGE), help="image to segment")
    args = parser.parse_args()

    pose_model = PoseDetector(str(POSE_MODEL), str(POSE_JSON))
    global sam_predictor
    sam_predictor = Predictor(str(RESNET_ENGINE), str(SAM_ENGINE))

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    while True:
        r, cvimg = cap.read()
        if not r:
            continue
        print("captured")
        pasted_cvimg = process_frame(cvimg)
        pasted_cvimg = pasted_cvimg.astype(np.uint8)
        cv2.imshow("segmented", pasted_cvimg)
        key = cv2.waitKey(10)
        if key == ord("s"):
            cv2.imwrite("masks_3.png", pasted_cvimg)
        elif key == ord("q"):
            break
