#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np


class KittiStixelDataset(object):
    def __init__(self, data_path, ground_truth_path, phase="train", batch_size=32, transform=None):
        assert os.path.isdir(data_path)
        assert os.path.isfile(ground_truth_path)

        self._data_path = os.path.join(data_path, "kitti_stixel_images")
        self._ground_truth_path = ground_truth_path

        # each line in ground truth contains the following information
        # series_date series_id frame_id x y point_type(Train/Test)
        # Eg: 09_26 1 55 242 Train
        lines = [line.rstrip("\n") for line in open(self._ground_truth_path, "r")]
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
            for line in lines if line[5] == phase_dict[phase]
        ]
        del lines

        self._image_dict = {}
        for line in self._lines:
            cur_base_image_path = self._generate_image_path_from_series_info(
                line["series_data"], line["series_id"], line["frame_id"]
            )
            if cur_base_image_path in self._image_dict.keys():
                self._image_dict[cur_base_image_path].append([line["x"], line["y"]])
            else:
                self._image_dict[cur_base_image_path] = []
        self._image_paths = list(self._image_dict.keys())
        self._stixels_pos = list(self._image_dict.values())

    def _generate_image_path_from_series_info(self, series_data, series_id, frame_id):
        base_image_name = "{:010d}.png".format(frame_id)
        base_image_dir = "2011_{}/2011_{}_drive_{:04d}_sync/image_02/data".format(series_data, series_data, series_id)
        base_image_path = os.path.join(base_image_dir, base_image_name)

        return base_image_path

    def __getitem__(self, idx):
        base_image_path = self._image_paths[idx]
        abs_image_path = os.path.join(self._data_path, base_image_path)
        cur_image = cv2.imread(abs_image_path)

        return cur_image, self._stixels_pos[idx]

    def __len__(self):
        return len(self._image_dict)

    def visualize_stixel(self, image, stixel_pos, stixel_width=5, stixel_height=100, color=(0, 255, 0)):
        result = np.copy(image)
        for (x, y) in stixel_pos:
            cv2.rectangle(result, (x, y - stixel_height), (x + stixel_width, y), color)

        return result

    def visualize_one_image(self, idx):
        assert idx < self.__len__()

        image, stixel_pos = self.__getitem__(idx)

        return self.visualize_stixel(image, stixel_pos)
