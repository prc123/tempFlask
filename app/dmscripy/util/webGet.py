import json
import datetime
import re
import time
import os
import requests
import urllib3
import copy
# import os
# import sys 
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) #当前程序上上一级目录，这里为mycompany

# sys.path.append(BASE_DIR)
from ...lib.bilibili_api import exceptions

request_settings = {
    "use_https": True,
    "proxies": None
}
urllib3.disable_warnings()

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}

MESSAGES = {
    "no_sess": "需要提供：SESSDATA（Cookies里头的`SESSDATA`键对应的值）",
    "no_csrf": "需要提供：csrf（Cookies里头的`bili_jct`键对应的值）"
}


def get_project_path():
    return os.path.dirname(__file__)

def get_api():
    """
    获取API
    :return:
    """
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/ViewApi.json"), "r", encoding="utf-8") as f:
        apis = json.loads(f.read())
        f.close()
    return apis

def request(method: str, url: str, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):

    if params is None:
        params = {}
    if data is None:
        data = {}
    if cookies is None:
        cookies = {}
    if headers is None:
        headers = copy.deepcopy(DEFAULT_HEADERS)
    if data_type.lower() == "json":
        headers['Content-Type'] = "application/json"
    st = {
        "url": url,
        "params": params,
        "headers": headers,
        "verify": request_settings["use_https"],
        "data": data,
        "proxies": request_settings["proxies"],
        "cookies": cookies
    }
    st.update(kwargs)

    req = requests.request(method, **st)
    time.sleep(0.1)

    if req.ok:
        content = req.content.decode("utf8")
        # if req.headers.get("content-length") == 0:
        #     return 

        if 'jsonp' in params and 'callback' in params:
            con = json.loads(re.match(".*?({.*}).*", content, re.S).group(1))
        else:
            con = json.loads(content)
        
        # if con["code"] != 0:
        #     if "message" in con:
        #         msg = con["message"]
        #     elif "msg" in con:
        #         msg = con["msg"]
        #     else:
        #         msg = "请求失败，服务器未返回失败原因"
        #     raise exceptions.BilibiliException(con["code"], msg)
        # else:
        
        
        return con
    else:
        raise exceptions.NetworkException(req.status_code)


def get(url, params=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用GET请求
    :param data_type:
    :param url:
    :param params:
    :param cookies:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("GET", url=url, params=params, cookies=cookies, headers=headers, data_type=data_type, **kwargs)

    return resp


def post(url, cookies=None, data=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用POST请求
    :param data_type:
    :param url:
    :param cookies:
    :param data:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("POST", url=url, data=data, cookies=cookies, headers=headers, data_type=data_type, **kwargs)
    return resp


def delete(url, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用DELETE请求
    :param data_type:
    :param url:
    :param params:
    :param data:
    :param cookies:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("DELETE", url=url, params=params, data=data, cookies=cookies, headers=headers, data_type=data_type, **kwargs)
    return resp

    