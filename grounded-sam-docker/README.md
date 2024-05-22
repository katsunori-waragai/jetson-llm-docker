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


## todo
- use stable opencv-python


