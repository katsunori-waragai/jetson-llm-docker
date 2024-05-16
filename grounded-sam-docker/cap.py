from pathlib import Path

import cv2

cap = cv2.VideoCapture(0)
oname = Path("captured/capture.jpg")
oname.parent.mkdir(exist_ok=True, parents=True)

while True:
    r, image = cap.read()
    oimg = image.copy()
    cv2.putText(oimg, "s: save", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0))
    cv2.putText(oimg, "q: quit", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0))
    cv2.imshow("image", oimg)
    key = cv2.waitKey(50)
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite(str(oname), image)
        print(f"saved {oname}")
        break
