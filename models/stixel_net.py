#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow.keras.models as models


def build_stixel_net(input_shape=(370, 800, 3)):
    """
    input_shape -> (height, width, channel)
    """
    img_input = keras.Input(shape=input_shape)

    x = layers.Conv2D(
        64, (3, 3), activation="relu", padding="same", name="block1_conv1"
    )(img_input)
    x = layers.Conv2D(
        64, (3, 3), activation="relu", padding="same", name="block1_conv2"
    )(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name="block1_pool")(x)

    # Block 2
    x = layers.Conv2D(
        128, (3, 3), activation="relu", padding="same", name="block2_conv1"
    )(x)
    x = layers.Conv2D(
        128, (3, 3), activation="relu", padding="same", name="block2_conv2"
    )(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name="block2_pool")(x)

    # Block 3
    x = layers.Conv2D(
        256, (3, 3), activation="relu", padding="same", name="block3_conv1"
    )(x)
    x = layers.Conv2D(
        256, (3, 3), activation="relu", padding="same", name="block3_conv2"
    )(x)
    x = layers.Conv2D(
        256, (3, 3), activation="relu", padding="same", name="block3_conv3"
    )(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name="block3_pool")(x)

    # Block 4
    x = layers.Conv2D(
        512, (3, 3), activation="relu", padding="same", name="block4_conv1"
    )(x)
    x = layers.Conv2D(
        512, (3, 3), activation="relu", padding="same", name="block4_conv2"
    )(x)
    x = layers.Conv2D(
        512, (3, 3), activation="relu", padding="same", name="block4_conv3"
    )(x)

    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.MaxPooling2D((2, 1), strides=(2, 1))(x)

    x = layers.Dropout(0.4)(x)

    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.MaxPooling2D((2, 1), strides=(2, 1), padding="same")(x)

    x = layers.Dropout(0.4)(x)

    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.MaxPooling2D((2, 1), strides=(2, 1))(x)

    x = layers.Dropout(0.4)(x)

    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(256, (3, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.MaxPooling2D((2, 1), strides=(2, 1))(x)

    x = layers.Dropout(0.4)(x)

    x = layers.Conv2D(2048, (3, 1), strides=(1, 1), padding="valid")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(2048, (1, 3), strides=(1, 1), padding="same")(x)
    x = layers.ELU()(x)
    x = layers.Conv2D(2048, (1, 1), strides=(1, 1))(x)
    x = layers.ELU()(x)

    x = layers.Dropout(0.4)(x)

    x = layers.Conv2D(50, (1, 1), strides=(1, 1), activation="softmax")(x)

    x = layers.Reshape((100, 50))(x)

    model = models.Model(inputs=img_input, outputs=x)

    return model
