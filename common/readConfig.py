#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser


class MyConfigParser:
    def __init__(self):
        self.cf = ConfigParser()

    def get_section_option_value(self, path, section, option):
        with open(path, encoding="utf-8") as f:
            self.cf.read(f)
            return self.cf.get(section, option)
