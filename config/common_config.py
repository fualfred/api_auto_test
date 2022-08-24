# !/usr/bin/python
# -*-coding:utf-8-*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
config = {
    "test_data_path": os.path.join(os.path.join(BASE_DIR, "testData"), "BThermostat"),
    "out_put_dir": os.path.join(os.path.join(BASE_DIR, "testCases"), "BThermostat")
}
print(os.path.join(os.path.join(BASE_DIR, "testData"), "BThermostat"))
print(os.path.join(os.path.join(BASE_DIR, "testCases"), "BThermostat"))
