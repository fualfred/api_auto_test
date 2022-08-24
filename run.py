#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
from common.utils import Utils
from common.logger import logger
import os
from config.common_config import config


def main():
    test_data_path = config.get("test_data_path")
    logger.info(f"--测试数据的路径是{test_data_path}")
    logger.info("--读取测试yml文件---")
    test_data = Utils.get_test_data(test_data_path)
    logger.info(f"读取的yml文件列表是\n{str(test_data)}")
    out_put_dir = config.get("out_put_dir")
    logger.info(f"测试用例目录是{out_put_dir}")
    logger.info(f"先删除之前生成的pytest脚本")
    Utils.remove_old_script(out_put_dir)
    logger.info(f"正在生成pytest测试脚本")
    for data in test_data:
        logger.info(f"在生成{data}的测试脚本")
        Utils.generate_test_script_by_jinja2(data, out_put_dir)
    logger.info(f"格式化测试脚本……")
    for root, dirs, files in os.walk(out_put_dir):
        logger.info(f"root:{root}---dirs:{dirs}--files:{files}")
        map(Utils.beautify_test_case_file, [os.path.join(root, file) for file in files if file.startswith("test")])
    logger.info(f"格式化测试脚本完成……")
    logger.info(f"pytest脚本生成完成")
    logger.info(f"开始执行pytest测试脚本")
    pytest.main()
    logger.info(f"pytest测试脚本执行完成")


if __name__ == "__main__":
    main()
