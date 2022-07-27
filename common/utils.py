#!/usr/bin/python
# -*- coding: utf-8 -*-
import jsonpath
import re
import os
import json
from hamcrest import *
from common.logger import logger
from common.envData import EnvData
import common.expand as Expand
from common.readYaml import ReadYaml
import jinja2
import subprocess

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__TEST_CASE_TEMPLATE__ = jinja2.Template(

"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import json
from common.utils import Utils, project_dir
from common.apiRequests import ApiRequest
from common.logger import logger

test_data_path = project_dir + "/testData/" + "{{yaml_file_name}}"


class {{test_class_name}}:

    @pytest.mark.parametrize("test_case", Utils.get_test_cases(test_data_path))
    def {{test_method}}(self, test_case, base_url):

        request_data = json.dumps(test_case)
        request_data = Utils.replace_request_data(request_data)
        method = request_data["method"]
        uri = request_data["uri"]
        mime_type = request_data["mime_type"]
        payload = request_data
        files = request_data["files"] if "files" in test_case else None
        extract = request_data["extract"] if "extract" in test_case else None
        validate = request_data["validate"] if "validate" in test_case else None

        response = ApiRequest(base_url).send(
            method, uri, mime_type, headers=None, payload=payload, files=files
        )

        if extract:
            logger.info(f"--要提取的数据---{extract}")
            Utils.extract(response, extract)
        if validate:
            logger.info(f"--预期验证的数据---{validate}")
            Utils.validate(response, validate)
"""
)


class Utils:

    @staticmethod
    def get_test_cases(path):
        test_cases = list()
        test_cases_dict = ReadYaml.read(path)
        if not test_cases_dict:
            logger.info("读取测试用例出错，请检查yaml文件")
        for key, value in test_cases_dict.items():
            if key == "testCases":
                for val in test_cases_dict["testCases"]:
                    # print(type(val["testCase"]))
                    test_cases.append(val["testCase"])
        return test_cases

    @staticmethod
    def validate(response, validate: list):
        for val in validate:
            for key, item in val.items():
                for key_json_path, item_expect in item.items():
                    logger.info(f"预期结果的值是{item_expect}")
                    actual_val = jsonpath.jsonpath(response, key_json_path)[0]
                    logger.info(f"获取真实值是{actual_val}")
                    if key == "equal_to":
                        assert_that(actual_val, equal_to(item_expect))
                    elif key == "not_equal_to":
                        assert_that(actual_val, is_not(equal_to(item_expect)))
                    elif key == "less_than":
                        assert_that(actual_val, less_than(item_expect))
                    elif key == "greater_than":
                        assert_that(actual_val, greater_than(item_expect))
                    elif key == "has_length":
                        assert_that(actual_val, has_length(item_expect))
                    elif key == "has_string":
                        assert_that(actual_val, has_string(item_expect))
                    elif key == "greater_than_or_equal_to":
                        assert_that(actual_val, greater_than_or_equal_to(item_expect))
                    elif key == "less_than_or_equal_to":
                        assert_that(actual_val, less_than_or_equal_to(item_expect))
                    elif key == 'not_none':
                        assert_that(actual_val, not_none())
                    else:
                        logger.info("-------暂时不支持该断言方法---------")

    @staticmethod
    def extract(response, extract: dict):
        for key, val in extract.items():
            set_value = jsonpath.jsonpath(response, val)[0]
            logger.info(f"提取的值是{set_value}")
            setattr(EnvData, key, set_value)

    # 替换变量${a} 或者函数$Fn{a(a,b)}
    @staticmethod
    def replace_request_data(request_data: str):
        def _decode(o):
            if isinstance(o, str):
                try:
                    return int(o)
                except ValueError:
                    return o
            elif isinstance(o, dict):
                return {k: _decode(v) for k, v in o.items()}
            elif isinstance(o, list):
                return [_decode(v) for v in o]
            else:
                return o

        logger.info(f"要替换的数据\n{request_data}")
        regex = r"\$\{.+?\}|\$Fn\{.+?\}"
        regex_obj = re.compile(regex)
        replace_values = regex_obj.findall(request_data)
        logger.info(f"要替换的值{str(replace_values)}")
        for val in replace_values:
            if "$Fn" not in val:
                key = val[2:-1]
                request_data = request_data.replace(f"{val}", str(getattr(EnvData, key)))
            else:
                val_str = val[4:-1]
                start_param_position = 0
                end_param_position = 0
                method = ''
                for i in range(len(val_str)):
                    if val_str[i] == '(':
                        method = val_str[0:i]
                        start_param_position = i
                    if val_str[i] == ')':
                        end_param_position = i
                params = val_str[start_param_position + 1: end_param_position]
                params = params.split(',')
                method_name = getattr(Expand, method)
                result = method_name(*params)
                logger.info(f"获取的参数是{params}，方法是{method_name},计算结果{result}")
                request_data = request_data.replace(f"{val}", str(result))
        logger.info(f"替换后的数据是\n{request_data}")
        return json.loads(request_data, object_hook=_decode)

    # @staticmethod
    # def generate_test_script(yml_file_name: str, out_put_dir):
    #     test_class = yml_file_name.split(".")[0]
    #     test_class_name_list = test_class.split("_")
    #     test_class_name = test_class_name_list[0].capitalize() + test_class_name_list[1].capitalize()
    #     template_path = os.path.join(project_dir, "test_template.txt")
    #     template_file = open(template_path, "r", encoding="utf-8")
    #     lines = template_file.readlines()
    #     out_put_file_path = out_put_dir + "/" + yml_file_name.replace(".yml", ".py")
    #     out_put_file = open(out_put_file_path, "a", encoding="utf-8")
    #     for line in lines:
    #         if "%fileName" in line:
    #             line = line.replace("%fileName", yml_file_name)
    #         if "%testClassName" in line:
    #             line = line.replace("%testClassName", test_class_name)
    #         if "%testMethod" in line:
    #             line = line.replace("%testMethod", test_class)
    #         out_put_file.write(line)
    #     out_put_file.close()

    @staticmethod
    def get_test_data(data_dir):
        file_list = list()
        for root, dirs, files in os.walk(data_dir, topdown=False):
            for name in files:
                file_list.append(name)
        return file_list

    @staticmethod
    def remove_old_script(out_put_dir):
        for root, dirs, files in os.walk(out_put_dir, topdown=False):
            for name in files:
                if "test_" in name:
                    os.remove(os.path.join(root, name))

    @staticmethod
    def generate_test_script_by_jinja2(yml_file_name: str, out_put_dir):

        test_class = yml_file_name.split(".")[0]
        test_class_name_list = test_class.split("_")
        test_class_name = test_class_name_list[0].capitalize() + test_class_name_list[1].capitalize()
        out_put_file_path = out_put_dir + "/" + yml_file_name.replace(".yml", ".py")
        out_put_file = open(out_put_file_path, "a", encoding="utf-8")
        reder_data = {
            "yaml_file_name": yml_file_name,
            "test_class_name": test_class_name,
            "test_method": test_class
        }
        content = __TEST_CASE_TEMPLATE__.render(reder_data)
        out_put_file.write(content)
        out_put_file.close()

    @staticmethod
    def beautify_test_case_file(file_path: str):
        logger.info("格式化测用例 ...")
        try:
            subprocess.run(["black", file_path])
        except subprocess.CalledProcessError as ex:
            logger.error(ex)
        except OSError:
            logger.error("OSError")
