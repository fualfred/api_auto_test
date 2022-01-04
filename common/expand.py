#!/usr/bin/python
# -*- coding: utf-8 -*-

def add(a, b):
    if not isinstance(a, int):
        a = int(a)
    if not isinstance(b, int):
        b = int(b)
    return a + b
