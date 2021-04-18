import requests
import copy
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/",
    "connection":"close"
}
class defauleRqu(object):
    def __init__(self):
        pass
    def request(self,method: str, url: str, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
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
            "verify": True,
            "data": data,
            "proxies": None,
            "cookies": cookies
        }
        st.update(kwargs)

        return requests.request(method, **st)