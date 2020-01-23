#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K


class StixelLoss(object):
    def __init__(self, num_bins=50, alpha=1.0, epsilon=0.0001):
        self._num_bins = num_bins
        self._alpha = alpha
        self._epsilon = epsilon

    def __call__(self, predict, target):
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

        fp = tf.gather(predict, K.cast(tf.math.floor(stixel_pos), dtype="int32"), batch_dims=-1)
        cp = tf.gather(predict, K.cast(tf.math.ceil(stixel_pos), dtype="int32"), batch_dims=-1)

        p = fp * (tf.math.ceil(stixel_pos) - stixel_pos) + cp * (
            stixel_pos - tf.math.floor(stixel_pos)
        )

        loss = -K.log(p) * have_target
        loss = K.sum(loss) / K.sum(have_target)

        return loss * self._alpha


if __name__ == '__main__':
    sl = StixelLoss()

    np.random.seed(100)
    predict = K.variable(np.random.rand(32, 100, 50))

    stixel_pos = K.variable(np.random.rand(32, 100, 1) * 50)
    stixel_pos = K.clip(stixel_pos, 0.51, 49.49)

    have_target = K.variable(np.random.rand(32, 100, 1))
    have_target = K.round(have_target)

    target = tf.stack((have_target, stixel_pos), axis=2)
    target = K.reshape(target, (32, 100, 2))

    loss = sl(predict, target)
    print(loss)
