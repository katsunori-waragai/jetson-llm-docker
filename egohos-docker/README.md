# docker for EgoHOS
- 自己視点画像での腕検出と対象物の検出
- 対象物は1st orderと 2nd orderとがある。

## original repo
https://github.com/owenzlz/EgoHOS

## 手順
```commandline
sh docker_build.sh
sh docker_run.sh

```
## Dockerfile の中で実行していること
- 一連のdownload の実行

## docker 環境内での作業
- python3を実行するようにすること。
- 修正済みのscriptのgit clone 先への重ね書き
- 自作scriptのgit clone 先への重ね書き
  - 自前動画のダウンロードとその動画への推論の実行

## 足りないと感じているもの
- 腕や手の関節の位置を出すことが含まれていない。
- まして、その３D版もない。
- これだけ、ハンドを動作させることはできない。
- 1st, 2nd order interacting object が名何かを教えてくれない。 

```commandline
cd mmsegmentation # if you are not in this directory
sed -i 's/python /python3 /g' pred_all_obj1.sh
bash pred_all_obj1.sh

```


## todo
- conversion to TRT

## troubleshooting
- 検出結果を保存する際にastype(dtype=np.uint8)を指定すること。