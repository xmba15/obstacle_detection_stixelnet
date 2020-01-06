#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np


class KittiStixelDataset(object):
    def __init__(self, data_path, ground_truth_path):
        assert os.path.isdir(data_path)
        assert os.path.isfile(ground_truth_path)

        self.__data_path = data_path
        self.__ground_truth_path = ground_truth_path

        # each line in ground truth contains the following information
        # series_date series_id frame_id x y point_type(Train/Test)
        # Eg: 09_26 1 55 242 Train
        lines = [line.rstrip("\n") for line in open(self.__ground_truth_path, "r")]
        assert len(lines) > 0
        lines = [line.split("\t") for line in lines]

        self.__lines = [
            {
                "series_data": line[0],
                "series_id": int(line[1]),
                "frame_id": int(line[2]),
                "x": int(line[3]),
                "y": int(line[4]),
                "type": line[5],
            }
            for line in lines
        ]
        del lines

        self.__image_dict = {}
        for line in self.__lines:
            cur_base_image_path = self.__generate_image_path_from_series_info(
                line["series_data"], line["series_id"], line["frame_id"]
            )
            if cur_base_image_path in self.__image_dict.keys():
                self.__image_dict[cur_base_image_path].append([line["x"], line["y"]])
            else:
                self.__image_dict[cur_base_image_path] = []
        self.__image_paths = list(self.__image_dict.keys())
        self.__stixels_pos = list(self.__image_dict.values())

    def __generate_image_path_from_series_info(self, series_data, series_id, frame_id):
        base_image_name = "{:010d}.png".format(frame_id)
        base_image_dir = "2011_{}/2011_{}_drive_{:04d}_sync/image_02/data".format(series_data, series_data, series_id)
        base_image_path = os.path.join(base_image_dir, base_image_name)

        return base_image_path

    def __getitem__(self, idx):
        base_image_path = self.__image_paths[idx]
        abs_image_path = os.path.join(self.__data_path, base_image_path)
        cur_image = cv2.imread(abs_image_path)

        return cur_image, self.__stixels_pos[idx]

    def __len__(self):
        return len(self.__image_dict)

    def visualize_stixel(self, image, stixel_pos, stixel_width=5, stixel_height=100, color=(0, 255, 0)):
        result = np.copy(image)
        for (x, y) in stixel_pos:
            cv2.rectangle(result, (x, y - stixel_height), (x + stixel_width, y), color)

        return result

    def visualize_one_image(self, idx):
        assert(idx < self.__len__())

        image, stixel_pos = self.__getitem__(idx)

        return self.visualize_stixel(image, stixel_pos)
