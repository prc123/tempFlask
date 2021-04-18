import requests
import json
import datetime
from tqdm import tqdm
import re
import pandas as pd
import bs4
import os
import time
from  lib_git.videoDownload.bilibili_video_download_v3 import *
class spiderClass():
    # 基本类
    def __init__(self,cookies):
        self.__cookies=self.format_cookie(cookies)
    def format_cookie(self,cookie_str):
        cookies = {}
        for line in cookie_str.split(';'):
            key,value=line.split('=')
            cookies[key]=value
        return cookies
    def getcookie(self):
        return self.__cookies
    def editcookies(self,cookies):
        sucess=True
        if isinstance(cookies,str):
            self.__cookies=self.format_cookie(cookies)
        elif isinstance(cookies,dict):
            self.__cookies=cookies
        else:
            print("The type of cookie is worry!")
            sucess=False
        return sucess

    def getUrl(sef,url, params=None, **kwargs):

        while True:
            try:
                res= requests.get(url,params, **kwargs)
                return res,res.status_code
            except Exception as e:
                # self.log.error("requests: %s error: %s" % (url, str(e)))
                print("requests: %s error: %s" % (url, str(e)))
                return res,res.status_code


class spider_BliBli(spiderClass):
    def __init__(self,cookies,url="https://www.bilibili.com/",videourl="https://www.bilibili.com/video/",apiurl="https://api.bilibili.com/x/player/" ,headers={
            'Host': 'api.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }):
        """
        docstring
        """
        super().__init__(cookies)
        self.AvBv()
        self.url=url
        self.videourl=videourl
        self.apiurl=apiurl
        self.headers=headers
    #根据bv号获取cid
    @staticmethod
    def getMainPage():
        while True:
            try:
                headers={
                'Host': 'www.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
                res= requests.get('https://www.bilibili.com',params=headers)
                return res,res.status_code
            except Exception as e:
                # self.log.error("requests: %s error: %s" % (url, str(e)))
                print("requests: %s error: %s" % (url, str(e)))
                return res,res.status_code
    def get_cid(self,bv):
        cid_url = f'https://api.bilibili.com/x/player/pagelist?bvid={bv}'
        res = requests.get(cid_url)
        res_text=res.text
        res_dict=json.loads(res_text)
        part_list = res_dict['data']
        new_part_list=[]
        for part in part_list:
            new_part={'cid':part.get('cid'),'part_name':part.get('part')}
            new_part_list.append(new_part)
        return new_part_list

    def get_status(self,bv):
        aid=self.dec(bv)
        info_data={}
        headers = {
            'Host': 'api.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        info = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
        info_rsp,status =self.getUrl(url=info,headers=headers)
        return info_rsp,status

    def get_view(self,bv):
        headers = {
        'Host': 'api.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
        info =' https://api.bilibili.com/x/web-interface/view?bvid='+ bv
        info_rsp,status = self.getUrl(url=info, headers=headers)
        return info_rsp,status


    def get_video_page(self,bv):
        cid_url = f'{self.videourl}{bv}'
        headers = {
            # 'Host': 'api.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        res ,status =self.getUrl(cid_url,headers=headers)
        res_html=""
        status=res.status_code
        res_html=res.text
        return res_html,status

    def get__one_month_data_list(self,cid,month):
        #https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=6534573&month=2020-12

        data_list_url = f'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={cid}&month={month}'
        res ,status= self.getUrl(data_list_url,cookies=self.getcookie())
        # res_dict=json.loads(res.text)
        # data_list=res_dict.get('data')
        return res,status
    def get_dan_mu_xml(self,cid,date):
        # https://api.bilibili.com/x/v2/dm/history?type=1&oid=6534573&date=2020-12-25
        dan_mu_url = f'https://api.bilibili.com/x/v2/dm/history?type=1&oid={cid}&date={date}'
        # dan_mu_url = f'https://ap.bilibili.com/x/v2/dm/history?type=1&oid={cid}&date={date}'
        res,_=self.getUrl(dan_mu_url,cookies=self.getcookie())
        da_mu_xml=res.content.decode('utf8')
        return da_mu_xml

    def get_comment(self,bv,page,sort_status=0,sleeptime=0.05):
        av=self.dec(bv)
        url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={av}&sort={sort_status}&nohot=1'
        headers = {
            # 'Host': 'api.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        proxy="60.169.115.234"
        proxies={
        'http':'http://'+proxy,
        'https':'https://'+proxy
        }
        # req,_ = self.getUrl(url,headers=headers,proxies=proxies)
        req,_ = self.getUrl(url,headers=headers,proxies=None)
        res_html = req.text
        print(url)
        time.sleep(sleeptime)
        return req

    def AvBv(self):
        self.table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        self.tr = {}
        for i in range(58):
            self.tr[self.table[i]] = i
        self.s = [11, 10, 3, 8, 4, 6]
        self.xor = 177451812
        self.add = 8728348608

    def dec(self,x):
        r=0
        for i in range(6):
            r+=self.tr[x[self.s[i]]]*58**i
        return (r-self.add)^self.xor

    def enc(self,x):
        x=(x^self.xor)+self.add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]]=self.table[x//58**i%58]
        return ''.join(r)

class Date_BliBli_Bv(object):
    """
    针对单个视频的数据类
    """
    pageStatus={"hot": 2,"time":0}
    def __init__(self,bv,spider,mkBvDir=False):
        self.bv=bv
        self.spider=spider
        self.setAll()

        # self.dirs=self.mkBvDir(bv)
    def setAll(self):
        #TOD        self.mkBvDir()O 某些设置
        pass
    # def mkBvDir(self, bv,path=""):
    #     pathList=[path,bv]
    #     if path!="":
    #         dirs="/".join(pathList)
    #     else:
    #         dirs=bv
    #     if not os.path.exists(dirs):
    #         os.makedirs(f'{dirs}')
    #     return dirs
    def saveCsv(self,df,filename,dirs=""):
        if dirs!="":
            dirs=dirs
        else:
            dirs=self.bv
        if not os.path.exists(dirs):
            os.makedirs(f'{dirs}')
        path=[dirs,filename]
        pathDate='/'.join(path)
        df.to_csv(f'{pathDate}', index=False)
        return df
    def getVideoPage(self):
        videoPage,_= self.spider.get_video_page(self.bv)
        # info_json = info_rsp.json()
        # info_data=info_json['data']
        return videoPage
    def getcommentPageNum(self):
        json_text=self.get_comment(1)
        # print(json_text)
        commentsNum = json_text["data"]["page"]["count"]
        listnum=json_text["data"]["page"]["size"]
        pagenum = commentsNum // listnum + 1
        return pagenum

    def getBvView(self):
        info_rsp,_= self.spider.get_view(self.bv)
        info_json = info_rsp.json()
        info_data=info_json['data']
        return info_data
    def getBvStaus(self):
        info_rsp,_= self.spider.get_status(self.bv)
        info_json = info_rsp.json()
        info_data=info_json['data']
        return info_data
    def getBvtoAid(self):
        return self.spider.dec(self.bv)
    def getBvCid(self):
         return self.spider.get_cid(self.bv)
    def get__one_month_data_list(self,cid,month):
        #https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=6534573&month=2020-12
        res ,_= self.spider.get__one_month_data_list(cid,month)
        res_dict=json.loads(res.text)
        data_list=res_dict.get('data')
        return data_list
    def get_data_history(self,cid_data_list,pubdate,enddate):
        date_history_list=[]
        end= enddate
        pudtime =pubdate
        for cid_item in cid_data_list:
            year = end.year
            month = end.month
            start_year = pudtime.year
            start_mounth = pudtime.month
            #pre_month_last_day = now.date()
            pre_month_last_day = end.date()
            while pre_month_last_day>pudtime.date():
                one_month_date_list = self.get__one_month_data_list(cid_item['cid'],f'{year}-{month:>02}')
                # print(one_month_date_list)
                if one_month_date_list:
                    cid_item['date_list']=cid_item.get('date_list',[])
                    cid_item['date_list'].extend(one_month_date_list)
                this_month_first_day=datetime.date(year,month,1)
                #print(this_month_first_day)
                pre_month_last_day=this_month_first_day-datetime.timedelta(days=1)
                year=pre_month_last_day.year
                month=pre_month_last_day.month
            date_history_list.append(cid_item)
        return  date_history_list
    def get_dan_mu_from_history(self,data_historry_list,toCsv=False):
        bv=self.bv
        df_list=[]
        for item in data_historry_list:
            part_name = item.get('part_name')
            part_name=part_name.replace('.','_')
            filename = bv
            all_dm_list=[]
            if part_name:
                filename=f'{bv}_{part_name}.csv'
            #with open(f'{filename}.txt','w',encoding='utf8') as f:
            for date in tqdm(item['date_list']):
                dan_mu_xml=self.spider.get_dan_mu_xml(item['cid'],date)
                # print(dan_mu_xml)
                dan_mu_list=self.parse_dan_mu(dan_mu_xml)
                # print(dan_mu_list)
                all_dm_list.extend(dan_mu_list)
                #print(dan_mu_list[0])
                # for dan_mu_item in dan_mu_list:
                #     line = '<;>'.join(dan_mu_item)
                #     f.writelines(line)
            #     f.write('\n')
            df=pd.DataFrame(all_dm_list,columns=['time','sendtime','dmtype','id','content'])
            if toCsv:
                self.saveCsv(df,filename)
            df_list.append(df)
        return df_list

#获取所有的弹幕列表时间
    def get_data_all_history(self):
        view=self.getBvView()
        pubdate=view['pubdate']
        now_date=view['ctime']
        cid_data_list=self.getBvCid()
        pubdate= datetime.datetime.fromtimestamp(pubdate)
        now_date=datetime.datetime.now()
        return self.get_data_history(cid_data_list,pubdate,now_date)

    def parse_dan_mu(self,get_dan_mu_xml):
        #print(_get_dan_mu_xml)
        reg=re.compile('<d p="([\s\S]*?)">([\s\S]+?)</d>')

        find_result=reg.findall(get_dan_mu_xml)

        dan_mu_list=[]
        for line in find_result:
            p,dan_mu=line
            print(line)
            dm_time=float(p.split(',')[0])

            time_stamp = int(p.split(',')[4])
            dm_type = int(p.split(',')[5])
            dm_id=p.split(',')[6]
            date_array=datetime.datetime.fromtimestamp(time_stamp)
            send_time=date_array.strftime('%Y-%m-%d %H:%M:%S')
            dan_mu_list.append([dm_time,send_time,dm_type,dm_id,dan_mu])
        return dan_mu_list


    #获取所有弹幕
    def getAllDanMu(self,toCsv=False):
        data_historry_list = self.get_data_all_history()
        return self.get_dan_mu_from_history(data_historry_list,toCsv)
    #根据时间获取弹幕
    def get_dan_mu_date(self,start_time,end_time,toCsv=False):
        view=self.getBvView()
        pubdate=view['pubdate']
        cid_data_list=self.getBvCid()
        pubdate= datetime.datetime.fromtimestamp(pubdate)
        now_date=datetime.datetime.now()
        data_historry_list=self.get_data_history(cid_data_list,start_time,end_time)
        return self.get_dan_mu_from_history(data_historry_list,toCsv)
    #获取前三十天弹幕
    def get_first_thirtyday_dm(self):
        view=self.getBvView()
        pubdate=view['pubdate']
        now_date=view['ctime']
        cid_data_list=self.getBvCid()
        pubdate= datetime.datetime.fromtimestamp(pubdate)
        end_date=pubdate+datetime.timedelta(days=30)

        return self.get_dan_mu_date(pubdate,end_date)
    #获取评论
    def get_comment(self,page,status=pageStatus["hot"]):
        comment=self.spider.get_comment(self.bv,page,status)
        json_response = comment.content.decode()
        json_text = json.loads(json_response)
        return json_text

    #获取评论的回复默认只显示3条
    def get_replies(self,data,info_list,page):
        n=page
        if data['replies']==None:
            return
        else:
            for replies in data['replies']:
                info_list.append([replies["member"]["uname"],replies["member"]["sex"], replies["content"]["message"], replies['like'],replies['rpid'],replies['root'],replies['ctime'],n])
                self.get_replies(replies, info_list,n)
        return info_list
    def get_page_comment(self,start,end,status=2,toCsv=False):
        maxpage=self.getcommentPageNum()
        info_list=[]
        tmp_df=None
        bv=self.bv
        filename=f'{bv}_comment.csv'
        # if start>0 and end>=start and end<=maxpage :
        end= end if end<maxpage else maxpage
        for n in tqdm(range(start, end+1)):
            comment=self.get_comment(n,status)
            self.get_replies(comment["data"],info_list,n)
        tmp_df=pd.DataFrame(info_list,columns=['uname','sex','message','like','rpid','root','ctime','page'])
        if toCsv:
            self.saveCsv(tmp_df,filename)
        return tmp_df
    def get_all_comment(self,status=2,toCsv=False):
        start=1
        end=self.getcommentPageNum()
        return self.get_page_comment(start,end,status=status,toCsv=False)
    def get_hundred_comment(self,status=2,toCsv=False):
        start=1
        end=start+100
        return self.get_page_comment(start,end,status=status,toCsv=False)
    def downloadVideo(self,quality=16):
        status=self.spider.dec(self.bv)
        downVideos(status,quality)


# class Video_BliBli_Bv(object):
#     def __init__(self):


    
def test1():
    cookie_str="""_uuid=BED55778-6C63-8EB8-5CF8-9BD4747381A936584infoc; buvid3=E48ED472-8EA8-416B-B0D1-B8EF7C910077138394infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k)~u~)~||l0J'uY|lYkYlmm; sid=kg46boin; DedeUserID=18783699; DedeUserID__ckMd5=da48a4965ebcb26b; SESSDATA=1adfb0d6%2C1621262055%2Cfd431*b1; bili_jct=b6238e6a4fbc8e4762cd3ca2fedd5893; CURRENT_QUALITY=116; fingerprint3=adaae4b2bd58211198cdf7e7d3d59d92; buvid_fp_plain=E48ED472-8EA8-416B-B0D1-B8EF7C910077138394infoc; buivd_fp=E48ED472-8EA8-416B-B0D1-B8EF7C910077138394infoc; fingerprint=2397befb0dca765aac88d87310b568cd; fingerprint_s=82af1bf1bd313260a7b7724f71fd3ab6; bsource=search_baidu; bp_t_offset_18783699=473813190004704279; PVID=1; bp_video_offset_18783699=474104122504750806"""
    # cookie_str=""
    test=spider_BliBli(cookie_str)
    a,b=test.getMainPage()
    print(a.text)
    bv1="BV1L64y1F7H5"
    bv2="BV1ky4y1e7qm"
    # print(test.getcookie())
    # bv=Date_BliBli_Bv(bv2,test)
    # view=bv.getBvView()
    # pubdate=view['pubdate']
    # pubdate=datetime.datetime.fromtimestamp(pubdate)
    # # print(pubdate,pubdate+datetime.timedelta(days=1))
    # # print(bv.get_dan_mu_date(pubdate,pubdate+datetime.timedelta(days=1)))
    # bv.downloadVideo()
    # print(bv.getBvView())
    # print(bv.getVideoPage())
    # print(bv.get_comment(1))
    # print(bv.getcommentPageNum())
    # print(bv.get_page_comment(1,1))
    #print(bv.get_hundred_comment())
if __name__ == "__main__":
    test1()