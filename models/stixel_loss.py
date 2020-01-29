#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from keras.losses import Loss
import keras.backend as K


class StixelLoss(Loss):
    def __init__(
        self, num_bins=50, alpha=1.0, epsilon=0.0001, label_size=(100, 50)
    ):
        super(StixelLoss, self).__init__(name="stixel_loss")
        self._num_bins = num_bins
        self._alpha = alpha
        self._epsilon = epsilon
        self._label_size = label_size

    def call(self, target, predict):
        """
        predict -> (h, w, num_bins)
        target -> (h, w, 2)
        """

        have_target, stixel_pos = tf.split(target, 2, axis=-1)
        stixel_pos = stixel_pos - 0.5
        stixel_pos = (
            (stixel_pos - tf.math.floor(stixel_pos))
            + tf.math.floor(stixel_pos)
            + self._epsilon
        )

        fp = tf.gather(
            predict,
            K.cast(tf.math.floor(stixel_pos), dtype="int32"),
            batch_dims=-1,
        )
        cp = tf.gather(
            predict,
            K.cast(tf.math.ceil(stixel_pos), dtype="int32"),
            batch_dims=-1,
        )

        p = fp * (tf.math.ceil(stixel_pos) - stixel_pos) + cp * (
            stixel_pos - tf.math.floor(stixel_pos)
        )

        loss = -K.log(p) * have_target
        loss = K.sum(loss) / K.sum(have_target)

        return loss * self._alpha

    def get_config(self):
        config = {
            "num_bins": self._num_bins,
            "alpha": self._alpha,
            "epsilon": self._epsilon,
            "label_size": self._label_size,
        }

        base_config = super(StixelLoss, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
