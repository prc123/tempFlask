import requests
from ..util.webGet import  get_api,get,post,exceptions

class spiderBiliChannle():
    def __init__(self):
        pass

    @staticmethod
    def getChannleRank(tid: int, day: int = 7):
        API = get_api()["channelView"]
        url = API["ranking"]["get_top10"]["url"]
        if day not in (3, 7):
            raise exceptions.BilibiliApiException("day只能是3，7")
        params = {
            "rid": tid,
            "day": day
        }
        resp = get(url=url, params=params)
        return resp

    @staticmethod
    def getChannleDynamic(tid: int, ps: int = 10):
        API = get_api()["channelView"]
        url = API["dynamic"]["url"]
        params = {
            "rid": tid,
            "ps": ps
        }
        resp = get(url=url, params=params)
        return resp

    # @staticmethod
    # def getpage