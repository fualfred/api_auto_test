# coding =utf-8
import requests
from requests_toolbelt import MultipartEncoder
import os
import random
import json
import simplejson
from common.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common.decorator import logger_send


class ApiRequest:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def __init__(self, base_url):
        self._base_url = base_url

    # 封装发送请求
    @logger_send
    def send(self, method: str, uri: str, mime_type: str, headers=None, payload=None, files=None):
        logger.info(f"请求uri是{uri}")
        logger.info(f"请求方法是{method}")
        logger.info(f"请求参数是{payload}")
        if headers is None:
            headers = {}
        if method.upper() == "POST":
            return self.post(uri, mime_type, headers=headers, payload=payload, files=files)
        elif method.upper() == "GET":
            return self.get(uri, mime_type, headers=headers, payload=payload)
        elif method.upper() == "PUT":
            return self.put(uri, mime_type, headers=headers, payload=payload, files=files)
        elif method.upper() == "DELETE":
            return self.delete(uri, mime_type, headers=headers, payload=payload)
        else:
            logger.error(f"{method}参数传递错误，暂时不支持该请求方法")
            return None

    # 封装post
    def post(self, uri: str, mime_type: str, headers: dict, payload: dict, files=None):
        """
        :param uri:    请求地址
        :param mime_type: 请求参数格式（form_data,raw）
        :param headers:    请求头
        :param payload: 请求参数
        :param files: 上传文件请求格式（dict）

        """
        if "http" in uri or "https" in uri:
            url = uri
        else:
            url = self._base_url + uri
        if 'form_data' in mime_type:
            for key in files:
                value = files[key]
                if '/' in value:
                    files[key] = (os.path.basename(value), open(value, 'rb'))
            enc = MultipartEncoder(
                fields=files,
                boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
            )
            headers['Content-type'] = enc.content_type
            res = requests.post(url=url, data=enc, headers=headers, verify=False)
        elif 'application/json' in mime_type:
            res = requests.post(url=url, json=payload, headers=headers, files=files, verify=False)
        else:
            res = requests.post(url=url, data=payload, headers=headers, files=files, verify=False)
        try:
            if res.status_code != 200:
                return res.text
            else:
                return res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            logger.exception('ERROR')
            logger.error(e)
            raise

    # 封装get
    def get(self, uri: str, mime_type: str, headers: dict, payload: dict):
        if "http" in uri or "https" in uri:
            url = uri
        else:
            url = self._base_url + uri
        if 'application/json' in mime_type:
            res = requests.get(url=url, headers=headers, json=payload, verify=False)
        else:
            res = requests.get(url=url, headers=headers, params=payload, verify=False)
        try:
            if res.status_code != 200:
                return res.text
            else:
                return res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            logger.exception('ERROR')
            logger.error(e)
            raise

    # 封装put
    def put(self, uri: str, mime_type: str, headers: dict, payload: dict, files=None):
        if "http" in uri or "https" in uri:
            url = uri
        else:
            url = self._base_url + uri
        if 'form_data' in mime_type:
            for key in files:
                value = files[key]
                if '/' in value:
                    files[key] = (os.path.basename(value), open(value, 'rb'))
            enc = MultipartEncoder(
                fields=files,
                boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
            )
            headers['Content-type'] = enc.content_type
            res = requests.put(url=url, data=enc, headers=headers, verify=False)
        elif 'application/json' in mime_type:
            res = requests.put(url=url, json=payload, headers=headers, files=files, verify=False)
        else:
            res = requests.put(url=url, data=payload, headers=headers, files=files, verify=False)
        try:
            if res.status_code != 200:
                return res.text
            else:
                return res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            logger.exception('ERROR')
            logger.error(e)
            raise

    # 封装delete
    def delete(self, uri: str, mime_type: str, headers: dict, payload: dict):
        if "http" in uri or "https" in uri:
            url = uri
        else:
            url = self._base_url + uri
        if 'application/json' in mime_type:
            res = requests.delete(url=url, headers=headers, json=payload, verify=False)
        else:
            res = requests.delete(url=url, headers=headers, params=payload, verify=False)
        try:
            if res.status_code != 200:
                return res.text
            else:
                return res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            logger.exception('ERROR')
            logger.error(e)
            raise
