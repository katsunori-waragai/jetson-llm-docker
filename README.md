# nanoowl-docker
docker for nanoowl

## 目標
− nanoowl をjetson AGX OrinでDocker環境下で動作させること。
- [nanoowl](https://github.com/NVIDIA-AI-IOT/nanoowl)

## Dockerfile
- 上記のnanoowl でのinstall 手順をDockerファイルに記述中

## docker環境内で行なっている処理
### torch2trt の install
```commandline
# cd /root/torch2trt/
# python3 setup.py install
# pip3 list | grep torch
```
torch2trt が表示されていれば、torch2trt のインストールには成功している。

### nanoowl の install
- 以下のインストール作業をdocker環境内で行なっている場合、毎回行うこと。

```commandline
cd /root/nanoowl/
python3 setup.py develop --user
mkdir -p data
python3 -m nanoowl.build_image_encoder_engine     data/owl_image_encoder_patch32.engine
```

### nanoowl の実行
```commandline
cd examples
python3 owl_predict.py     --prompt="[an owl, a glove]"     --threshold=0.1     --image_encoder_engine=../data/owl_image_encoder_patch32.engine

ls ../data
```

owl_predict_out.jpg が作成されていれば成功。

## nanoowl になれるには
- 以下のURLのREADME.md を読むこと
https://github.com/NVIDIA-AI-IOT/nanoowl

# このリポジトリを作った理由
- https://github.com/NVIDIA-AI-IOT/nanoowl/tree/main にdocker/23-01 があるが
- sh build.sh の動作に成功していない。
- そのため、自分でdocker環境を構築することにした。


## TODO
- bash docker_build.sh の際にエラーを生じる。(tensortrtをdocker build 中に利用しようとした場合)
- Libnvdla_compiler.so error on nvidia jetson container
https://forums.developer.nvidia.com/t/libnvdla-compiler-so-cannot-open-shared-object-file-no-such-file-or-directory/240750

### Libnvdla_compiler.so error 問題の切り分け
- docker run 後には生じていない。
  - そのため、tensorrt を使う処理はdocker環境内で実行している。
- host環境では問題を生じていない。
```commandline
$ python3
>>> import tensorrt

```

### nanoowl に関する日本語記事
- https://techblog.cccmkhd.co.jp/entry/2023/12/19/112221
