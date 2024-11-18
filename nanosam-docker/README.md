# docker for nanosam

#### Important
Link to pre-trained model (resnet18_image_encoder.onnx) is broken.
https://github.com/NVIDIA-AI-IOT/nanosam

So I included the pretrained models using Git LFS.

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

#### pre-trained モデル
```commandline
data/mobile_sam_mask_decoder.engine
data/mobile_sam_mask_decoder.onnx
data/resnet18_image_encoder.engine
data/resnet18_image_encoder.onnx
```

上記のファイルがGoogle Drive からダウンロードできるはずのもの。
しかし、2024年11月時点ではダウンロードできなかった。
Jetson へのnanosam の移植は、Docker　imageが用意されていた。
`dustynv/nanosam:r36.2.0`

このdocker環境を立ち上げると
```commandline
data/mobile_sam_mask_decoder.engine
data/mobile_sam_mask_decoder.onnx
data/resnet18_image_encoder.engine
data/resnet18_image_encoder.onnx
```
のファイルが含まれていた。
これらのファイルをscpでホスト環境に持ち出すことができる。



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

2024/11の時点で、セグメンテーションのコードは動作している。
しかし、ポーズを利用するコードは、モデルファイルがダウンロードできないため、動作していない。
densenet121_baseline_att_256x256_B_epoch_160.pth

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

####
```commandline
 python3 my_segment_from_pose.py 
/usr/local/lib/python3.8/dist-packages/torchvision-0.14.1a0+5e8e2f1-py3.8-linux-aarch64.egg/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/usr/local/lib/python3.8/dist-packages/torchvision-0.14.1a0+5e8e2f1-py3.8-linux-aarch64.egg/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=DenseNet121_Weights.IMAGENET1K_V1`. You can also use `weights=DenseNet121_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
Downloading: "https://download.pytorch.org/models/densenet121-a639ec97.pth" to /root/.cache/torch/hub/checkpoints/densenet121-a639ec97.pth
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 30.8M/30.8M [00:06<00:00, 5.06MB/s]
Traceback (most recent call last):
  File "my_segment_from_pose.py", line 105, in <module>
    pose_model = PoseDetector(str(POSE_MODEL), str(POSE_JSON))
  File "/root/nanosam/nanosam/utils/trt_pose.py", line 50, in __init__
    self.model.load_state_dict(torch.load(weights))
  File "/usr/local/lib/python3.8/dist-packages/torch/serialization.py", line 786, in load
    with _open_file_like(f, 'rb') as opened_file:
  File "/usr/local/lib/python3.8/dist-packages/torch/serialization.py", line 270, in _open_file_like
    return _open_file(name_or_buffer, mode)
  File "/usr/local/lib/python3.8/dist-packages/torch/serialization.py", line 251, in __init__
    super().__init__(open(name, mode))
FileNotFoundError: [Errno 2] No such file or directory: '/root/nanosam/data/densenet121_baseline_att_256x256_B_epoch_160.pth'

```

densenet121のモデルのダウンロードと利用の関係がつじつまがあっていない。
そのため、実行時のエラーを生じている。

## 以下のモデルファイルのダウンロード
- trt-pose を使うセグメンテーションの実行時に利用する。
`nanosam/examples/segment_from_pose.py`

densenet121_baseline_att_256x256_B_epoch_160.pth 
以下の場所からダウンロードできる。
https://github.com/NVIDIA-AI-IOT/trt_pose


 [Import Error] Unable to import tensorrt inside pytorch:2.1-r36.2.0 #472 
https://github.com/dusty-nv/jetson-containers/issues/472

```commandline
python3 -m pip install tensorrt
Collecting tensorrt
  Downloading tensorrt-10.6.0.tar.gz (16 kB)
  Preparing metadata (setup.py) ... done
Collecting tensorrt-cu12==10.6.0 (from tensorrt)
  Downloading tensorrt-cu12-10.6.0.tar.gz (18 kB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [6 lines of output]
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "/tmp/pip-install-ahhg6ijg/tensorrt-cu12_951ba6738311462090e07de3dd83d493/setup.py", line 71, in <module>
          raise RuntimeError("TensorRT does not currently build wheels for Tegra systems")
      RuntimeError: TensorRT does not currently build wheels for Tegra systems
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

```

