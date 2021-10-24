#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
from common.utils import Utils
from common.utils import project_dir
from common.logger import logger


def main():
    test_data_path = project_dir + "/testData"
    logger.info(f"--测试数据的路径是{test_data_path}")
    logger.info("--读取测试yml文件---")
    test_data = Utils.get_test_data(test_data_path)
    logger.info(f"读取的yml文件列表是\n{str(test_data)}")
    out_put_dir = project_dir + "/testCases"
    logger.info(f"测试用例目录是{out_put_dir}")
    logger.info(f"先删除之前生成的pytest脚本")
    Utils.remove_old_script(out_put_dir)
    logger.info(f"正在生成pytest测试脚本")
    for data in test_data:
        logger.info(f"在生成{data}的测试脚本")
        Utils.generate_test_script(data, out_put_dir)
    logger.info(f"pytest脚本生成完成")


if __name__ == "__main__":
    main()
    pytest.main()