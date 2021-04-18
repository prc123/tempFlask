import requests
from ..util.webGet import  get_api,get,post,exceptions
from ...lib.bilibili_api import video ,utils,common
from datetime import datetime
import time
import pandas as pd
# def get_play_list(start_url, cid, quality):
#     entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
#     appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
#     params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
#     chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
#     url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
#     headers = {
#         'Referer': start_url,  # 注意加上referer
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
#     }
#     # print(url_api)

#     html = requests.get(url_api, headers=headers).json()
#     print(json.dumps(html))
#     video_list = []
#     for i in html['durl']:
#         video_list.append(i['url'])
#     # print(video_list)
#     return video_list

class spiderVideoinfo():
    def __init__(self):
        pass

    @staticmethod
    def getVideoInfo(bvid: str = None, aid: int = None, is_simple: bool = False, verify: utils.Verify = None):
        """
        获取视频信息
        :param aid:
        :param bvid:
        :param is_simple: 简易信息（另一个API）
        :param verify:
        :return:
        """
        return video.get_video_info(bvid, aid, is_simple, verify)

    @staticmethod
    def getTags(bvid: str = None, aid: int = None, verify: utils.Verify = None):
        """
        获取视频标签
        :param aid:
        :param bvid:
        :param verify:
        :return:
        """
        
        resp = video.get_tags(bvid, aid, verify)
        return resp

    @staticmethod
    def getChargers(bvid: str = None, aid: int = None, verify: utils.Verify = None):
        """
    获取视频充电用户
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
        get = video.get_chargers(bvid, aid, verify)
        return get

    @staticmethod
    def getRelated(bvid: str = None, aid: int = None, verify: utils.Verify = None):
        """
        获取该视频相关推荐
        :param aid:
        :param bvid:
        :param verify:
        :return:
        """
        get = video.get_related(bvid, aid, verify)
        return get
    @staticmethod
    def getCommentsG(bvid: str = None, aid: int = None, order: str = "time", verify: utils.Verify = None):
        """
        获取该视频相关评论
        :param aid:
        :param bvid:
        :param verify:
        :return:
        """
        replies=video.get_comments_main(bvid,aid,order)
        # get_comments_main
        # a=[]
        # for i in range(3):
        #     a.append(next(replies))
        return replies

    @staticmethod
    def getVideoUrl(bvid: str = None, aid: int = None, verify: utils.Verify = None):
        """
        获取该视频相关评论
        :param aid:
        :param bvid:
        :param verify:
        :return:
        """
        replies=video.get_download_url(bvid,aid)
        # get_comments_main
        # a=[]
        # for i in range(3):
        #     a.append(next(replies))
        return replies

    @staticmethod
    def getVideoDm(bvid: str = None, aid: int = None, oid: int = 0,
                              date= None, verify = None):
        """
        获取该视频相关弹幕
        :param aid:
        :param bvid:
        :param verify:
        :return:
        """
        # replies=video.get_history_danmaku_index(bvid, aid, 0,
        #                       date, verify)
        # tmpDmInfo=[]
        # for i in replies:
        # date=datetime.strptime(i,"%Y-%m-%d")
        tmp=video.get_danmaku_g(bvid, aid, oid,verify, date)
        time.sleep(0.5)
        # tmpDmInfo={"dm_time":[],"send_time":[],"dm_type":[],"dm_id":[],"dm_text":[]} 
        tmpDmInfo=[]    
        for data in tmp:
            tmpDm=[data.dm_time.seconds,data.send_time,data.mode,data.id_str,data.text]
            tmpDmInfo.append(tmpDm)
        df=pd.DataFrame(tmpDmInfo,columns=['time','sendtime','dmtype','id','content'])
        return df
        # df=pd.DataFrame(tmpDmInfo,columns=['time','sendtime','dmtype','id','content'])
        # dfJson=df.to_json(orient="columns",force_ascii=False)
        # return dfJson
        # get_comments_main
        # a=[]
        # for i in range(3):
        #     a.append(next(replies))
        # return df