# !/usr/bin/python
# -*-coding:utf-8-*-
import jinja2
TEST_CASE_TEMPLATE = jinja2.Template(
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import json
from common.utils import Utils, project_dir
from common.apiRequests import ApiRequest
from common.logger import logger
from config.common_config import config

test_data_path = config.get("test_data_path")+"/"+"{{yaml_file_name}}"


class {{test_class_name}}:

    @pytest.mark.parametrize("test_case", Utils.get_test_cases(test_data_path))
    def {{test_method}}(self, test_case, base_url):

        request_data = json.dumps(test_case, ensure_ascii=False)
        request_data = Utils.replace_request_data(request_data)
        method = request_data["method"]
        uri = request_data["uri"]
        mime_type = request_data["mime_type"]
        payload = request_data["payload"]
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
