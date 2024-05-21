## grounded-SAM docker
- docker environment for grounded SAM
https://github.com/IDEA-Research/Grounded-Segment-Anything

### Dockerファイル内での処理
- GroundedSAMを使うための環境構築
- GroundedSAMを使うためのpre-trained file のダウンロード
- ユーザー作成ファイルのCOPY

### status
sh docker_build.sh 
sh docker_run.sh
succeeded.

## usage
### test_cap_and_demo.sh
USBカメラから1枚画像を取得して、その画像に対して、grounded-SAMのdemo相当の処理を行う。

### run_usbcam.sh
- USBカメラ　入力でのセグメンテーション


### test_pre-captured.sh
- capture済の画像をセグメンテーションする。

### grounded_sam_demo.py
- 元からあるdemo スクリプト
```
python3 grounded_sam_demo.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
   --grounded_checkpoint groundingdino_swint_ogc.pth \
   --sam_checkpoint sam_vit_h_4b8939.pth \
   --input_image images/ego4d_2d386a76-9ef1-49ff-982e-d5e403bba456_12750.jpg \
   --output_dir "outputs" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "arm . door " \
   --device "cuda"
```

```
python3  grounded_sam_demo.py -h
usage: Grounded-Segment-Anything Demo [-h] --config CONFIG --grounded_checkpoint GROUNDED_CHECKPOINT
                                      [--sam_version SAM_VERSION] [--sam_checkpoint SAM_CHECKPOINT]
                                      [--sam_hq_checkpoint SAM_HQ_CHECKPOINT] [--use_sam_hq] --input_image INPUT_IMAGE
                                      --text_prompt TEXT_PROMPT --output_dir OUTPUT_DIR [--box_threshold BOX_THRESHOLD]
                                      [--text_threshold TEXT_THRESHOLD] [--device DEVICE]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       path to config file
  --grounded_checkpoint GROUNDED_CHECKPOINT
                        path to checkpoint file
  --sam_version SAM_VERSION
                        SAM ViT version: vit_b / vit_l / vit_h
  --sam_checkpoint SAM_CHECKPOINT
                        path to sam checkpoint file
  --sam_hq_checkpoint SAM_HQ_CHECKPOINT
                        path to sam-hq checkpoint file
  --use_sam_hq          using sam-hq for prediction
  --input_image INPUT_IMAGE
                        path to image file
  --text_prompt TEXT_PROMPT
                        text prompt
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory
  --box_threshold BOX_THRESHOLD
                        box threshold
  --text_threshold TEXT_THRESHOLD
                        text threshold
  --device DEVICE       running on cpu only!, default=False
```

## todo
- use stable opencv-python


