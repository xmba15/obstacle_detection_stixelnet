#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import Config
import argparse
import numpy as np
import cv2
from models import build_stixel_net
from data_loader import KittiStixelDataset
from albumentations import (
    Compose,
    Resize,
    Normalize,
)
import tensorflow.keras.backend as K


parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_path", required=True
)
# parser.add_argument(
#     "--image_path", re=True
# )
parsed_args = parser.parse_args()


def test_single_image(model, img, label_size=(100, 50)):
    assert img is not None

    h, w, c = img.shape
    val_aug = Compose([Resize(370, 800) ,Normalize(p=1.0)])
    aug_img = val_aug(image=img)["image"]
    aug_img = aug_img[np.newaxis, :]
    predict = model.predict(aug_img, batch_size=1)
    predict = K.reshape(predict, label_size)
    predict = K.eval(K.argmax(predict, axis= -1))

    for x, py in enumerate(predict):
        x0 = int(x * w / 100)
        x1 = int((x + 1) * w / 100)
        y = int((py + 0.5) * h / 50)
        cv2.rectangle(img, (x0, 0), (x1, y), (0, 0, 255), 1)

    return img

def main(args):
    assert os.path.isfile(args.model_path)
    # assert os.path.isfile(args.image_path)

    dt_config = Config()
    model = build_stixel_net()
    model.load_weights(args.model_path)
    val_set = KittiStixelDataset(
        data_path=dt_config.DATA_PATH,
        ground_truth_path=dt_config.GROUND_TRUTH_PATH,
        phase="val",
        batch_size=1,
        input_shape=None
    )
    img, _ = val_set[500]
    img = img[0]

    result = test_single_image(model, img)
    cv2.imwrite("result5.png", result)


if __name__ == '__main__':
    main(parsed_args)
