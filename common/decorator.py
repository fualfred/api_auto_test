#!/usr/bin/python
# -*- coding: utf-8 -*-


def logger_send(func):
    from common.logger import logger

    def wrapper(*args, **kwargs):
        if len(args) > 0:
            logger.info(f"请求的方法是：{args[1]}")
            logger.info(f"请求的uri是：{args[2]}")
            logger.info(f"请求的Content-Type是：{args[3]}")
        if len(kwargs) > 0:
            if kwargs["headers"]:
                logger.info(f"请求头headers是：{kwargs['headers']}")
            if kwargs["payload"]:
                logger.info(f"请求数据是：\n{kwargs['payload']}")
            if kwargs["files"]:
                logger.info(f"上传的文件数据是：\n{kwargs['files']}")
        data = func(*args, **kwargs)
        logger.info(f"返回的响应数据是：\n{data}")
        return data

    return wrapper
