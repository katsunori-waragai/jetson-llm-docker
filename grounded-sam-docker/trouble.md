# trouble
- [x] --text_prompt で指定した内容に対して検出結果がないと、grounded_sam_demo.py は異常終了しないように対策する。
- [x] H, W をheight, widthの意味になるようにして、かつ従来通りのセグメンテーションの描画になるように修正する。
- [x] grounded_sam_output.jpg 中の原画像由来の領域を原画像の色順序に一致させる。
- [x] 保存するファイル名についての制約を減らす。保存する関数でのsignature の変更
- [x] changed output file names as follows
- [x] --image_dir を指定して入力フォルダ単位で処理するように改変した。
- [x] cap.py も複数の画像を保存できるよう改変した。
- [] sam が標準のsamを使っているのをnanoSAMを使うように改変して処理時間を減らそう。
- [] grounding の処理時間は、２回め以降は1 [s] 以下になっている。
- [] 後処理の時間がmatplotlibでかかりすぎているのを改善しよう。
```commandline
outputs/demo1_mask.jpg
outputs/demo1_mask.json
outputs/demo1_raw.jpg
outputs/demo1_sam.jpg
```

- 1枚の画像だけ処理するスクリプトはオーバーヘッドが大きすぎる。
