#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


class StixelLoss(object):
    def __init__(self, num_bins=50, alpha=1.0):
        self._num_bins = num_bins
        self._alpha = alpha

    def __call(self, predict, target):
        """
        predict -> (h, w, num_bins)
        target -> (h, w, 2)
        """
        have_target = target[:, :, 0, np.newaxis]
        stixel_pos = target[:, :, 1, np.newaxis]

        stixel_pos=(stixel_pos-0.5)
