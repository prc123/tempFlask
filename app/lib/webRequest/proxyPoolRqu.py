from proxy_pool.handler.proxyHandler import ProxyHandler
import requests
import copy
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/",
    "connection":"close"
}

class proxyPoolRqu(object):
    def __init__(self):
        self.proxyHandler=ProxyHandler()
    def request(self,method: str, url: str, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
        proxy=self.proxyHandler.get()
        proxy= proxy.to_dict if proxy else None
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
            "proxies": {"http": "http://{proxy}".format(proxy=proxy['proxy']), "https": "https://{proxy}".format(proxy=proxy['proxy'])},
            "cookies": cookies,
        }
        st.update(kwargs)
        print(st["proxies"])
        return requests.request(method, **st)