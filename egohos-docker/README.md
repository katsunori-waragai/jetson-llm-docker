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
- シェルスクリプト内で起動するpythonはpython3と明示する。
そうでないと、python2.7が起動してしまう。
- python3を実行するようにすること。
- 修正済みのscriptのgit clone 先への重ね書き
- 自作scriptのgit clone 先への重ね書き
  - 自前動画のダウンロードとその動画への推論の実行

## 足りないと感じているもの
- 腕や手の関節の位置を出すことが含まれていない。
- まして、その３D版もない。
- これだけ、ハンドを動作させることはできない。
- 1st, 2nd order interacting object が何かを教えてくれない。 
- 物体をハンドリングしている手の場合だと、手の一部が隠れている。
  - その隠れている指の状態を予測することが大事となる。

```commandline
cd mmsegmentation # if you are not in this directory
sed -i 's/python /python3 /g' pred_all_obj1.sh
bash pred_all_obj1.sh

bash pred_all_obj2.sh

```

--mode two_hands_obj1 1st order interacting objects
--mode tow_hands_obj2 1st and 2nd order interacting objects
とがある。
ポットから鍋にお湯を注ぐ動作があるときには、ポットに手を触れているので、ポットが
1st order interacting objectになる。
対応して、--checkpoint_file に違いがある。


predict_obj1_videos.shの中で呼び出しているpredict_videos.py の中にpythonインタプリタをpythonとだけ記述してある部分があり、これもpython3 と明示的に指定する。


cbと略記されているのは
contact boundary である。
それによって、どの領域で手が対象物と触れているのかを把握できる。


### output 
testimages
testimages/images
testimages/pred_cb
testimages/pred_cb_vis
testimages/pred_obj1
testimages/pred_obj1_vis
testimages/pred_obj2
testimages/pred_obj2_vis
testimages/pred_twohands
testimages/pred_twohands_vis

## 動画での推論
- 動画はmp4のファイル形式をサポートしている。
  - webmなどのファイルは事前にmp4に変換しておく。


## todo
- conversion to TRT

## troubleshooting
- 検出結果を保存する際にastype(dtype=np.uint8)を指定すること。