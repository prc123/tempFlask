import os
import sys
import requests
from proxy_pool.handler import proxyHandler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SingletonType(type):
    def __init__(self,*args,**kwargs):
        super(SingletonType,self).__init__(*args,**kwargs)

    def __call__(cls, *args, **kwargs): # 这里的cls，即Foo类
        print('cls',cls)
        obj = cls.__new__(cls,*args, **kwargs)
        cls.__init__(obj,*args, **kwargs) # Foo.__init__(obj)
        return obj

class webRequest(metaclass=SingletonType):
    def __init__(self,setting):
        self.setting=setting
        self.proxy=setting["requestProxy"]
        self.type=setting["requestType"]
        self.__initwebRequest()
    def __initwebRequest(self):
        __type=None
        if self.proxy:
            if "PROXYPOOL"==self.type:
                __type="proxyPoolRqu"
            else:
                pass
        else:
            __type="defauleRqu"
        self.Rqu=getattr(__import__(__type), f"{__type}")()
    def request(self,method,**kwargs):
        return self.Rqu.request( method,**kwargs)
                