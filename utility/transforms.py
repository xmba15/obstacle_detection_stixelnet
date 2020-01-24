#!/usr/bin/env python
# -*- coding: utf-8 -*-


class HorizontalFlip(object):
    def __init__(self, p=0.5):
        self._p = p

    def __call__(self, image, target):
        assert target.ndim == 2 and target.shape[1] == 2

        import numpy as np
        if np.random.rand() <= self._p:
            return {"image": image[:, ::-1, :], "target": target[::-1, :]}
        else:
            return {"image": image, "target": target}
