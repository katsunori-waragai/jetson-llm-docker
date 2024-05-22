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
- [] sam が標準のsamを使っているのをnanoSAMを使うように改変して処理時間を減らそう。
- [] ファイルへの保存なしという選択もできるようにAPIを変更しよう。
- [] grounding の処理時間は、２回め以降は1 [s] 以下になっている。
- [] PIL.Image はAPIのインタフェースから外す。
- [] モジュールの外部で参照しないものは"_"始まりの変数名に変更する。
- [] testをきちんとtestにしよう。
- [] dino とsamの区別がつきやすい識別子にすること。
```commandline
outputs/demo1_mask.jpg
outputs/demo1_mask.json
outputs/demo1_raw.jpg
outputs/demo1_sam.jpg
```

- 1枚の画像だけ処理するスクリプトはオーバーヘッドが大きすぎる。


used_time={'grounding': 3.974650587, 'sam': 2.788701992, 'save_mask': 0.252452241, 'save_sam': 7.441547751, 'save_sam_blend': 0.107093193}
used_time={'grounding': 0.730599378, 'sam': 1.840278247, 'save_mask': 0.373110757, 'save_sam': 7.586116283, 'save_sam_blend': 0.102947056}
used_time={'grounding': 0.697567113, 'sam': 1.869858615, 'save_mask': 0.228883811, 'save_sam': 6.113102738, 'save_sam_blend': 0.128356961}
used_time={'grounding': 0.679329176, 'sam': 1.85770102, 'save_mask': 0.255273111, 'save_sam': 7.080752494, 'save_sam_blend': 0.171673654}
used_time={'grounding': 0.67732794, 'sam': 1.929674399, 'save_mask': 0.25038156, 'save_sam': 6.310392899, 'save_sam_blend': 0.128888416}
used_time={'grounding': 0.670407028, 'sam': 1.962717893, 'save_mask': 0.229111996, 'save_sam': 4.959611013, 'save_sam_blend': 0.106903298}

