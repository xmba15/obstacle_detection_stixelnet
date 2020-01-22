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
            (stixel_pos - tf.floor(stixel_pos))
            + tf.floor(stixel_pos)
            + self._epsilon
        )

        fp = self._custom_gather(predict, tf.floor(stixel_pos))
        cp = self._custom_gather(predict, tf.ceil(stixel_pos))

        p = fp * (tf.ceil(stixel_pos) - stixel_pos) + cp * (
            stixel_pos - tf.floor(stixel_pos)
        )

        loss = -K.log(p) * have_target
        loss = K.sum(loss) / K.sum(have_target)

        return loss * self._alpha

    def _custom_gather(self, predict, stixel_pos):
        # result = K.variable(shape=stixel_pos.shape)
        result = K.placeholder(shape=stixel_pos.shape)

        bs, dim1, _ = predict.shape.as_list()
        casted_stixel_pos = K.cast(stixel_pos, dtype="int32")
        # result[0][0][10] = casted_stixel_pos[0][0][0]

        for i in range(bs):
            for j in range(dim1):
                # result[i][j][0] = predict[i][j][
                #     casted_stixel_pos[i][j][0]
                # ]

                tf.assign(result[i][j][0], predict[i][j][
                    casted_stixel_pos[i][j][0]
                ])


        return result


if __name__ == '__main__':
    sl = StixelLoss()
    predict = K.variable(np.random.rand(32, 100, 50))
    target = K.variable(np.random.rand(32, 100, 2)) * 50
    target = K.clip(target, 0.51, 49.49)

    # sl(predict, target)
    have_target, stixel_pos = tf.split(target, 2, axis=-1)
    floor_stixel_pos = K.cast(tf.floor(stixel_pos), dtype="int32")

    # print(K.eval(tf.gather_nd(predict, floor_stixel_pos)[0][1]))

    print(K.eval(tf.gather(predict, floor_stixel_pos).shape))

    # print(K.eval(floor_stixel_pos[0][1][0]))

    # print(K.eval(predict[0][1][K.eval(floor_stixel_pos[0][1][0])]))
