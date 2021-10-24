#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
from common.logger import logger


class ReadYaml:
    @staticmethod
    def read(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data
        except Exception as e:
            logger.exception(f"请查看文件是否正确，异常信息是{str(e)}")
            return None
