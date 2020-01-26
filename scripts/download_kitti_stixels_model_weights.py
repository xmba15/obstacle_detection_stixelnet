#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import tqdm
import sys


_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(_CURRENT_DIR, "..")))
try:
    from utility import download_file_from_google_drive
except Exception as e:
    print("cannot import module")
    exit(0)


def main():
    data_path = os.path.abspath(os.path.join(_CURRENT_DIR, "../saved_models"))
    if not os.path.isdir(data_path):
        os.system("mkdir -p {}".format(data_path))

    file_id = "1xbn6O4GpQ2CjRkh-i-7eNfHDktA06hwY"
    destination = os.path.join(data_path, "model.h5")

    if not os.path.isfile(destination):
        print("start downloading weights...")
        download_file_from_google_drive(file_id, destination)
        print("finish downloading weights and save into {}".format(destination))


if __name__ == "__main__":
    main()
