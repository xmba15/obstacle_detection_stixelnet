#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow.keras as keras


class StixelNet(keras.Model):

    def __init__(self, input_size):
        super(StixelNet, self).__init__(name="stixel net")
        self._input_size = input_size

    def call(self, inputs):
        pass
