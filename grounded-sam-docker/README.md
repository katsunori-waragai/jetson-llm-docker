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
USBカメラから画像を取得・保存して、その画像に対して、grounded-SAMのdemo相当の処理を行う。

### run_usbcam.sh
- USBカメラ　入力でのセグメンテーション


### test_pre-captured.sh
- capture済の画像をセグメンテーションする。

### gsam.py
```commandline
python3 gsam.py -h
usage: gsam.py [-h] [--use_sam_hq] --image_dir IMAGE_DIR --text_prompt TEXT_PROMPT --output_dir OUTPUT_DIR
                                      [--box_threshold BOX_THRESHOLD] [--text_threshold TEXT_THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --use_sam_hq          using sam-hq for prediction
  --image_dir IMAGE_DIR
                        path to image file
  --text_prompt TEXT_PROMPT
                        text prompt
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory
  --box_threshold BOX_THRESHOLD
                        box threshold
  --text_threshold TEXT_THRESHOLD
                        text threshold

python3 gsam_movie.py -h
usage: gsam_movie.py [-h] [--use_sam_hq] --text_prompt TEXT_PROMPT --output_dir OUTPUT_DIR [--box_threshold BOX_THRESHOLD]
                     [--text_threshold TEXT_THRESHOLD]

Grounded-Segment-Anything for USB camera

optional arguments:
  -h, --help            show this help message and exit
  --use_sam_hq          using sam-hq for prediction
  --text_prompt TEXT_PROMPT
                        text prompt
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory
  --box_threshold BOX_THRESHOLD
                        box threshold
  --text_threshold TEXT_THRESHOLD
                        text threshold

```
## todo
- use stable opencv-python


