# from ..util.webrequest import *
import requests
from ..util.webGet import  get_api,get,post


class spiderBiliView(object):

    def __init__(self, *arg, **kwargs):
        pass

    @staticmethod
    def getDing():
        API = get_api()["biliView"]
        url = API["Ding"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getbanner():
        API = get_api()["biliView"]
        url = API["banner"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getSearchDeaultWords():
        API = get_api()["biliView"]
        url = API["getSearchDeaultWords"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getPromote():
        API = get_api()["biliView"]
        url = API["promote"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getTopbg():
        API = get_api()["biliView"]
        url = API["Topbg"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getHot():
        API = get_api()["biliView"]
        url = API["Hot"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getSlideShow():
        API = get_api()["biliView"]
        url = API["promote"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getSeason():
        API = get_api()["biliView"]
        url = API["Ding"]["url"]
        resp = get(url)
        return resp

    @staticmethod
    def getRecommend():
        API = get_api()["biliView"]
        url = API["recommend"]["url"]
        resp = get(url)
        return resp

    # @staticmethod
    # def getContenRank():
    #     API = get_api()["biliView"]
    #     url = API["rankbase"]["url"]
    #     resp = get(url)
    #     return  resp
    @staticmethod
    def getContenRank(data):
        API = get_api()["biliView"]
        url = API["rankbase"]["url"]
        resp=get(url)
        return  resp
    
    @staticmethod
    def getContenRankList(categoryId):
        API = get_api()["biliView"]
        rankbase = API["rankbase"]["url"]
        url= rankbase + str(categoryId) + '-3day.json'
        resp=get(url)
        return  resp

    @staticmethod
    def getContenRankWeek(categoryId):
        API = get_api()["biliView"]
        rankbase = API["rankbase"]["url"]
        url= rankbase + str(categoryId) + '-week.json'
        print(url)
        resp=get(url)
        return  resp
    
    @staticmethod
    def getWebLive():
        API = get_api()["biliView"]
        url = API["live"]["url"]
        resp=get(url)
        return  resp
    
