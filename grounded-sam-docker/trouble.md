# trouble
- [x] --text_prompt で指定した内容に対して検出結果がないと、grounded_sam_demo.py は異常終了しないように対策する。
- [x] H, W をheight, widthの意味になるようにして、かつ従来通りのセグメンテーションの描画になるように修正する。
- [x] grounded_sam_output.jpg 中の原画像由来の領域を原画像の色順序に一致させる。
- [x] 保存するファイル名についての制約を減らす。保存する関数でのsignature の変更
- [x] changed output file names as follows
- [x] --image_dir を指定して入力フォルダ単位で処理するように改変した。
- [x] cap.py も複数の画像を保存できるよう改変した。
- [x] 後処理の時間がmatplotlibでかかりすぎているのを改善しよう。
- [x] torch.Tensor をわかりやすくする。
- [x] dataclass　を実装する。
- [x] `from some import *` はなくすこと。
- [x] 実行ディレクトリを制約しないように書き換えること
- [x] argsの処理をclass に反映させよう。
- [x] dino とsamの区別がつきやすい識別子にすること。
- [x] モジュールの外部で参照しないものは"_"始まりの変数名に変更する。
- [] sam が標準のsamを使っているのをnanoSAMを使うように改変して処理時間を減らそう。
- [] ファイルへの保存なしという選択もできるようにAPIを変更しよう。
- [] grounding の処理時間は、２回め以降は1 [s] 以下になっている。
- [] PIL.Image はAPIのインタフェースから外す。
- [] testをきちんとtestにしよう。
- [] use_sam_hq=Trueとすると、何が良くなるはずかを記載する。
  - 木製のイスをセグメンテーションしている事例がある。 
  - 標準のSAMの出力では、イスの隙間で地面の芝生が見えている領域までイスと同一のセグメンテーションになっている。 
  - SAM-HQ Outputでは、イスの隙間越しに見える芝生の領域の多くが、イスのセグメンテーションから外れている。

- [] sam_hq_vit_h.pth をdownload して使えるようにすること
- https://github.com/SysCV/sam-hq#model-checkpoints
- huggingface からダウンロードできる。
- https://huggingface.co/lkeab/hq-sam/tree/main
- [] --input_image を使用している従来のスクリプトが使えていない。
```commandline
outputs/demo1_mask.jpg
outputs/demo1_mask.json
outputs/demo1_raw.jpg
outputs/demo1_sam.jpg
```

- 1枚の画像だけ処理するスクリプトはオーバーヘッドが大きすぎる。

used_time={'grounding': 4.601885602, 'sam': 2.78923419, 'save_mask': 0.223663634, 'save_sam': 0.101654286}
used_time={'grounding': 0.619241372, 'sam': 1.836635902, 'save_mask': 0.221149576, 'save_sam': 0.099712454}
used_time={'grounding': 0.509424686, 'sam': 1.837601291, 'save_mask': 0.193354196, 'save_sam': 0.098929636}
used_time={'grounding': 0.513645634, 'sam': 1.833863588, 'save_mask': 0.221209674, 'save_sam': 0.099474151}
used_time={'grounding': 0.583415437, 'sam': 1.867050265, 'save_mask': 0.205879691, 'save_sam': 0.099982281}
used_time={'grounding': 0.516912789, 'sam': 1.831642283, 'save_mask': 0.183015659, 'save_sam': 0.103907674}
