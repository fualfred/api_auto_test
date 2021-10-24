#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
from common.utils import project_dir, ReadYaml


def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.fixture(scope="session")
def base_url():
    config_file_path = project_dir + "/config/env.yml"
    config_data = ReadYaml.read(config_file_path)
    key = config_data["default"]
    return config_data["env"][key]