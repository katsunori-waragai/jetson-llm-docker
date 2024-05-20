import cv2
import numpy as np
import matplotlib.pyplot as plt

# 例として、セグメンテーション結果の2D numpy配列を作成します
# この配列は、セグメンテーションの結果を整数値として格納しています
segmentation_result = np.array([
    [0, 1, 2, 3],
    [2, 1, 0, 4],
    [1, 2, 0, 3],
    [4, 3, 1, 2]
], dtype=np.uint8)

# セグメンテーション結果に対して色を定義します
# 各整数値に対応するRGB色を定義します
COLOR_MAP = {
    0: [0, 0, 0],       # 黒
    1: [0, 255, 0],     # 緑
    2: [0, 0, 255],     # 青
    3: [255, 0, 0],     # 赤
    4: [255, 255, 0],   # 黄色
    5: [255, 0, 255],   # マゼンタ
    6: [0, 255, 255],   # シアン
    7: [128, 128, 128], # グレー
    8: [128, 0, 0],     # マルーン
    9: [128, 128, 0],   # オリーブ
    10: [0, 128, 0],    # ダークグリーン
    11: [0, 128, 128],  # ティール
    12: [0, 0, 128],    # ネイビー
    13: [255, 165, 0],  # オレンジ
    14: [255, 215, 0],  # ゴールド
    15: [173, 216, 230],# ライトブルー
    16: [75, 0, 130],   # インディゴ
    17: [240, 128, 128],# ライトコーラル
    18: [244, 164, 96], # サドルブラウン
    19: [60, 179, 113]  # ミディアムシーブルー
}

def colorize(segmentation_result: np.ndarray) -> np.ndarray:
    # カラー画像の初期化
    height, width = segmentation_result.shape
    color_image = np.zeros((height, width, 3), dtype=np.uint8)
    num_colors = len(COLOR_MAP)

    maxint = np.max(segmentation_result.flatten())
    # セグメンテーション結果をカラー画像にマッピング
    for i in range(maxint):
        color_image[segmentation_result == i] = COLOR_MAP[i % num_colors]
    return color_image

color_image = colorize(segmentation_result)
# 画像を表示
plt.imshow(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
plt.title('Segmented Image')
plt.show()
