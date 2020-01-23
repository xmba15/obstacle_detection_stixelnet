#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from tensorflow.python.keras.utils.data_utils import Sequence


class KittiStixelDataset(Sequence):
    def __init__(
        self,
        data_path,
        ground_truth_path,
        phase="train",
        batch_size=10,
        label_size=(100, 50),
        shuffle=True,
        transform=None,
        random_seed=2011,
        input_shape=(370, 800),
    ):
        """
        input_shape->(height,width)
        """
        super(KittiStixelDataset, self).__init__()

        assert os.path.isdir(data_path)
        assert os.path.isfile(ground_truth_path)

        self._data_path = os.path.join(data_path, "kitti_stixel_images")
        self._ground_truth_path = ground_truth_path
        self._batch_size = batch_size
        self._label_size = label_size
        self._shuffle = shuffle
        self._transform = transform
        self._input_shape = input_shape

        # each line in ground truth contains the following information
        # series_date series_id frame_id x y point_type(Train/Test)
        # Eg: 09_26 1 55 242 Train
        lines = [
            line.rstrip("\n") for line in open(self._ground_truth_path, "r")
        ]
        assert len(lines) > 0
        lines = [line.split("\t") for line in lines]

        assert phase in ("train", "val")
        phase_dict = {"train": "Train", "val": "Test"}
        self._lines = [
            {
                "series_data": line[0],
                "series_id": int(line[1]),
                "frame_id": int(line[2]),
                "x": int(line[3]),
                "y": int(line[4]),
                "type": line[5],
            }
            for line in lines
            if line[5] == phase_dict[phase]
        ]
        del lines

        self._image_dict = {}
        for line in self._lines:
            cur_base_image_path = self._generate_image_path_from_series_info(
                line["series_data"], line["series_id"], line["frame_id"]
            )
            if cur_base_image_path in self._image_dict.keys():
                self._image_dict[cur_base_image_path].append(
                    [line["x"], line["y"]]
                )
            else:
                self._image_dict[cur_base_image_path] = [[line["x"], line["y"]]]

        self._image_paths = list(self._image_dict.keys())
        self._stixels_pos = list(self._image_dict.values())
        self._indexes = np.arange(len(self._image_paths))

        np.random.seed(random_seed)

    @property
    def batch_size(self):
        return self._batch_size

    def _generate_image_path_from_series_info(
        self, series_data, series_id, frame_id
    ):
        base_image_name = "{:010d}.png".format(frame_id)
        base_image_dir = "2011_{}/2011_{}_drive_{:04d}_sync/image_02/data".format(
            series_data, series_data, series_id
        )
        base_image_path = os.path.join(base_image_dir, base_image_name)

        return base_image_path

    def __getitem__(self, idx):
        ids = self._indexes[
            idx * self._batch_size : (idx + 1) * self._batch_size
        ]

        X, y = self._data_generation(ids)

        return X, y

    def __len__(self):
        return int(np.floor(len(self._image_dict) / self._batch_size))

    def _data_generation(self, list_ids):
        if self._input_shape:
            X = np.stack(
                [
                    cv2.resize(
                        cv2.imread(
                            os.path.join(self._data_path, self._image_paths[idx])
                        ),
                        (self._input_shape[1], self._input_shape[0]),
                    )
                    for idx in list_ids
                ],
                axis=0,
            )
        else:
            X = np.stack(
                [
                    cv2.imread(
                        os.path.join(self._data_path, self._image_paths[idx])
                    )
                    for idx in list_ids
                ],
                axis=0,
            )


        if self._transform:
            X = np.stack(
                [self._transform(image=elem)["image"] for elem in X], axis=0
            )

        y = np.stack(
            [self._generate_label_image(idx) for idx in list_ids], axis=0
        )

        return X, y

    def _generate_label_image(self, idx):
        img = cv2.imread(os.path.join(self._data_path, self._image_paths[idx]))

        positions = np.array(self._stixels_pos[idx], dtype=np.float32)
        height, width = img.shape[:2]

        positions[:, 0] = positions[:, 0] / width
        positions[:, 1] = positions[:, 1] / height

        colnum, binnum = self._label_size
        have_gt = np.zeros((colnum), dtype=np.int)
        gt = np.zeros((colnum), dtype=np.float32)

        for point in positions:
            col_idx = int(point[0] * colnum)
            row_idx = point[1] * binnum

            if have_gt[col_idx] == 1:
                gt[col_idx] = (gt[col_idx] + row_idx) / 2
            else:
                gt[col_idx] = row_idx
                have_gt[col_idx] = 1

        gt = np.clip(gt, 0.51, 49.49)

        return np.stack((have_gt, gt), axis=1)

    def on_epoch_end(self):
        if self._shuffle:
            np.random.shuffle(self._indexes)

    def visualize_stixel(
        self,
        image,
        stixel_pos,
        stixel_width=5,
        stixel_height=100,
        color=(0, 255, 0),
    ):
        result = np.copy(image)
        [
            cv2.rectangle(
                result, (x, y - stixel_height), (x + stixel_width, y), color
            )
            for (x, y) in stixel_pos
        ]

        return result

    def visualize_one_image(self, idx):
        img = cv2.imread(
            os.path.join(
                self._data_path, self._image_paths[idx * self._batch_size]
            )
        )

        if self._transform:
            img = self._transform(image=img)["image"]

        stixel_pos = self._stixels_pos[idx * self._batch_size]

        return self.visualize_stixel(img, stixel_pos)
