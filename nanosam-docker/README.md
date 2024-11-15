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


# 動作検証用のデモプログラムの実行
```commandline
sh 5_demo.sh
```

- シェルスクリプトにハードコードされたように、TRTに変換済みのモデルを用いて、セグメンテーションを実行する。
- 入力静止画のpathと出力先は、examples/basic_usage.py の中にハードコーディングされている。


## example
```commandline
python3 examples/basic_usage.py \
    --image_encoder=data/resnet18_image_encoder.engine \
    --mask_decoder=data/mobile_sam_mask_decoder.engine
```

## 改変なしの便利なデモ
- nanosam/examples/demo_pose_tshirt.py
  Tshirt領域をセグメンテーションする。入力はカメラ入力。
## 改変したスクリプト
### my_basic_usage.py  
```commandline
python3 my_basic_usage.py -h
usage: my_basic_usage.py [-h] [--image_encoder IMAGE_ENCODER]
                         [--mask_decoder MASK_DECODER] [--image IMAGE]

optional arguments:
  -h, --help            show this help message and exit
  --image_encoder IMAGE_ENCODER
  --mask_decoder MASK_DECODER
  --image IMAGE         image to segment
```
- 引数で指定した静止画について指定のencoderを用いてセグメンテーションするスクリプト

### my_segment_from_pose.py
```commandline
python3 my_segment_from_pose.py -h 
usage: my_segment_from_pose.py [-h] [--camid CAMID] [--movie MOVIE]

optional arguments:
  -h, --help     show this help message and exit
  --camid CAMID  camera to segment
  --movie MOVIE  movie to segment
```
- webcamの画像から1人について、セグメンテーションを実施するスクリプト
- 上半身の衣類、下半身の衣類、肌色に見えている領域のセグメンテーションを実施する。
- そのためのヒントとして、人物のpose推定による関節の位置を利用している。

## 以下のモデルファイルのダウンロード
- trt-pose を使うセグメンテーションの実行時に利用する。
`nanosam/examples/segment_from_pose.py`

densenet121_baseline_att_256x256_B_epoch_160.pth 
以下の場所からダウンロードできる。
https://github.com/NVIDIA-AI-IOT/trt_pose


 [Import Error] Unable to import tensorrt inside pytorch:2.1-r36.2.0 #472 
https://github.com/dusty-nv/jetson-containers/issues/472
