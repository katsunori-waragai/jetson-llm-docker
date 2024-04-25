# docker for nanosam


## Original nanosam

https://github.com/NVIDIA-AI-IOT/nanosam/blob/main/README.md

## 手順

```
cd nanosam-docker/
sh docker_build.sh
sh docker_run.sh

cd /root/nanosam
```

# model file のダウンロード
- Google Drive からのmodel file のダウンロードは Dockerfile の中に記述した。
  - resnet18_image_encoder.onnx
  - densenet121_baseline_att_256x256_B_epoch_160.pth


# デモプログラムの実行
sh 5_demo.sh
```


## exmaple
python3 examples/basic_usage.py \
    --image_encoder=data/resnet18_image_encoder.engine \
    --mask_decoder=data/mobile_sam_mask_decoder.engine

## 改変したスクリプト
入力ファイルを変更したい。
- my_basic_usage.py  
- my_segment_from_pose.py

## TODO
- 入力ファイルを変更できること
- 入力をファイルではなく、webcam にできること
- TRT済みのモデルを使うようになっているかの確認
- なっていなければTRTに変更する


## 以下のモデルファイルのダウンロード
- trt-pose を使うセグメンテーションの実行時に利用する。
`nanosam/examples/segment_from_pose.py`

densenet121_baseline_att_256x256_B_epoch_160.pth 
以下の場所からダウンロードできる。
https://github.com/NVIDIA-AI-IOT/trt_pose
