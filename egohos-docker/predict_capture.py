from mmseg.apis import inference_segmentor, init_segmentor
import mmcv
import glob
import os
from tqdm import tqdm
import argparse
from PIL import Image
import numpy as np 
from skimage.io import imsave
import pdb
import cv2

"""
https://mmsegmentation.readthedocs.io/en/latest/migration/package.html?highlight=inference_segmentor#mmseg-apis

       --config_file ./work_dirs/twohands_cb_to_obj2_ccda/twohands_cb_to_obj2_ccda.py \
       --checkpoint_file ./work_dirs/twohands_cb_to_obj2_ccda/best_mIoU_iter_32000.pth \
              --pred_seg_dir ../testimages/pred_obj2
"""

parser = argparse.ArgumentParser(description="")
parser.add_argument("--config_file", default='./work_dirs/twohands_cb_to_obj2_ccda/twohands_cb_to_obj2_ccda.py')
parser.add_argument("--checkpoint_file", default='./work_dirs/twohands_cb_to_obj2_ccda/best_mIoU_iter_32000.pth')
# parser.add_argument("--img_dir", default='../data/train/image', type=str)
parser.add_argument("--pred_seg_dir", default='../testimages/pred_obj2')
args = parser.parse_args()

os.makedirs(args.pred_seg_dir, exist_ok = True)

# build the model from a config file and a checkpoint file
model = init_segmentor(args.config_file, args.checkpoint_file, device='cuda:0')

alpha = 0.5
cap = cv2.VideoCapture(0)
while True:
    r, cvimg = cap.read()
    file = "pred_twohands/tmp.png"
    cv2.imwrite(file, cvimg)
    # img = np.array(Image.open(file))
    # fileが引数になっている。
    seg_result = inference_segmentor(model, cvimg)[0]
    fname = file.split(".")[0]
    imsave(os.path.join(args.pred_seg_dir, fname + '.png'), seg_result.astype(np.uint8))

