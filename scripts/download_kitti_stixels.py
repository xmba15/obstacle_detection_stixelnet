#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import tqdm


_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in tqdm.tqdm(response.iter_content(CHUNK_SIZE)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


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
