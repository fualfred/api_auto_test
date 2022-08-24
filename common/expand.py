#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import hashlib
from typing import Union


# def time_stamp(s):
#     time_array = time.strptime(s, '%Y-%m-%d %H:%M')
#     return int(time.mktime(time_array))


def make_md5(input_val: Union[str, int]) -> str:
    md = hashlib.md5()
    if isinstance(input_val, int):
        input_val = str(input_val)
    md.update(input_val.encode("utf-8"))
    return md.hexdigest()


def get_current_time() -> int:
    # time.sleep(1)
    return int(time.time())


def make_trace_id(time_stamp: int) -> str:
    return make_md5(time_stamp)


def make_current_trace_id() -> str:
    return make_md5(get_current_time())


def get_chrome():
    from faker import Faker
    return Faker().chrome()
