# docker for EgoHOS
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
```commandline
cd mmsegmentation # if you are not in this directory
sed -i 's/python /python3 /g' pred_all_obj1.sh
bash pred_all_obj1.sh

```

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


## todo
- conversion to TRT

## troubleshooting
- 検出結果を保存する際にastype(dtype=np.uint8)を指定すること。
