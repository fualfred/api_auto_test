#!/usr/bin/python
# -*- coding: utf-8 -*-
from common.apiRequests import ApiRequest
import yaml
import re
import json
from common.utils import Utils

if __name__ == "__main__":
    api_request = ApiRequest("https://api2.mubu.com")
    method = "post"
    uri = "/v3/api/user/phone_login"
    mime_type = "application/json"
    headers = {}
    payload = {
        "phone": "13528872802",
        "password": "123456abc",
        "callbackType": 0
    }
    # headers = {"Connection": 'close'}
    # print(requests.get("https://baidu.com/",verify=False))
    # res = api_request.send("post", uri, mime_type, headers=headers, payload=payload, files=None)
    # print("res:", res)
    # with open("demo.yml", "r") as f:
    #     data = yaml.safe_load(f)
    #     print(type(data))
    #     print(json.dumps(data))
    a = "aaa${a}ssss$Fn{a(1,1)}dfdf"
    regex = r"\$\{.+?\}|\$Fn\{.+?\}"
    regex_obj = re.compile(regex)

    replace_values = regex_obj.findall(a)
    print(replace_values)
    # for val in replace_values:
    #     print(val[4:-1])
    # print(Utils.get_test_cases("demo.yml"))