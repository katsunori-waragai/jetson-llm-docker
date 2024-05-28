"""
SEE ALSO:
https://www.stereolabs.com/docs/depth-sensing/using-depth

https://github.com/stereolabs/zed-sdk/tree/master/tutorials/tutorial%203%20-%20depth%20sensing/python

https://stackoverflow.com/questions/67678048/whats-the-proper-way-to-colorize-a-16-bit-depth-image
"""

import inspect
from pprint import pprint

import pyzed.sl as sl

import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 opr HD1200 video mode, depending on camera type.
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use meter units (for depth measurements)
    init_params.camera_fps = 30  # Set fps at 30
    init_params.enable_right_side_measure = True
    print(f"{init_params=}")
    pprint(f"{inspect.getmembers(init_params)}")  # sl.RuntimeParameters() object のデータメンバーを表示させる。
    print("---")

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()


    # Capture 50 frames and stop
    i = 0
    image = sl.Mat()
    depth_map = sl.Mat()

    pprint(f"{inspect.getmembers(image)}")  # sl.Mat() object のデータメンバーを表示させる。
    print("---")

    runtime_parameters = sl.RuntimeParameters()
    pprint(f"{inspect.getmembers(runtime_parameters)}")  # sl.RuntimeParameters() object のデータメンバーを表示させる。
    print("---")

    while i < 5:
        # Grab an image, a RuntimeParameters object must be given to grab()

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH) # Retrieve depth
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
            print(f"Image resolution: {image.get_width()} x {image.get_height()} || Image timestamp: {timestamp.get_milliseconds()}\n")
            i = i + 1
            # print(f"{image=}")
            data = image.get_data()  # 戻り値が配列になる。
            data = cv2.cvtColor(data, cv2.COLOR_BGRA2RGBA)
            if i <= 1:
                print(f"{image.get_data_type()=}")
                print(f"{image.get_channels()=}")
                print(f"{image.get_height()=}")
                print(f"{image.get_width()=}")
                print(f"{image.get_infos()=}")

            depth_map_data = depth_map.get_data()
            if i <= 1:
                print(f"{depth_map_data.shape=}")
                print(f"{depth_map_data.dtype=}")  # expected to be "float32"
                print(f"{np.nanmin(depth_map_data.flatten())=}")
            plt.figure(1)
            plt.subplot(1, 2, 1)
            plt.imshow(data)
            plt.subplot(1, 2, 2)
            plt.imshow(depth_map_data, cmap="gist_rainbow")
            plt.colorbar()
            plt.draw()
            plt.pause(0.01)

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
