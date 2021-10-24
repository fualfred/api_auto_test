#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import json
import allure
from common.utils import Utils, project_dir
from common.apiRequests import ApiRequest
from common.logger import logger

test_data_path = project_dir + "/testData/" + "test_profile.yml"


class TestProfile:

    @pytest.mark.parametrize("test_case", Utils.get_test_cases(test_data_path))
    def test_profile(self, test_case, base_url):

        request_data = json.dumps(test_case)
        request_data = Utils.replace_request_data(request_data)
        test_case = json.loads(request_data)
        method = test_case["method"]
        uri = test_case["uri"]
        mime_type = test_case["mime_type"]
        payload = test_case["payload"]
        files = test_case["files"] if "files" in test_case else None
        extract = test_case["extract"] if "extract" in test_case else None
        validate = test_case["validate"] if "validate" in test_case else None

        response = ApiRequest(base_url).send(
            method, uri, mime_type, headers=None, payload=payload, files=files
        )

        if extract:
            logger.info(f"--要提取的数据---\n{extract}")
            Utils.extract(response, extract)
        if validate:
            logger.info(f"--预期验证的数据---\n{validate}")
            Utils.validate(response, validate)
