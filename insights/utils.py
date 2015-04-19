# -*- coding: utf-8 -*-
def first(arr, default=None):
    if not arr:
        return default

    return next(iter(arr))