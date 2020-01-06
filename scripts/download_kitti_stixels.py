#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, ".."))
try:
    from utility import download_file_from_google_drive
except Exception as e:
    print("cannot import module")
    exit(0)


def main():
    data_path = os.path.join(_CURRENT_DIR, "../data")
    file_id = "13heRc3iRHISjjsg1-ba2qk2fycznqFVc"
    destination = os.path.join(data_path, "kitti_stixel_images.zip")
    if not os.path.isfile(destination) and not os.path.isdir(
        os.path.join(data_path, "kitti_stixel_images")
    ):
        download_file_from_google_drive(file_id, destination)
        os.system(
            "cd {} && unzip kitti_stixel_images.zip -d .".format(data_path)
        )


if __name__ == "__main__":
    main()
