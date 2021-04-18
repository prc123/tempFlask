import requests
import json
import re
import datetime
import bs4
from tqdm import tqdm
from avtobv import AvBv
import time
import pandas as pd
import os
import numpy as np
cookies={}
remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~—◢—]+'
def format_cookie(cookie_str):
    cookies={}
    for line in cookie_str.split(';'):
        key,value=line.split('=')
        cookies[key]=value
    return cookies
def get_cid(bv):
    cid_url = f'https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp'
    res = requests.get(cid_url)
    res_text=res.text
    res_dict=json.loads(res_text)

    part_list = res_dict['data']
    new_part_list=[]
    for part in part_list:
        new_part={'cid':part.get('cid'),'part_name':part.get('part')}
        new_part_list.append(new_part)
    return new_part_list
def get_startday(bv):
    cid_url = f'https://www.bilibili.com/video/{bv}'
    res = requests.get(cid_url)
    res_html=res.text
    print(cid_url)
    #print(res.text)
    soup=bs4.BeautifulSoup(res_html,'lxml')
    mounth=soup.find('div',class_='video-data').find_all('span')[1].text.split(' ')[0]#.stripped_strings()

    aid=soup.find('meta',property='og:url')['content'].split('/')[-2].split('av')[-1]

    return aid,mounth
def get_aid(cid):
    aid_url=f'http://interface.bilibili.com/player?id=cid:{cid}'
    aid=requests.get(aid_url,cookies=cookies)
    print(aid_url)
    print(aid.text)
    return
def _get__one_month_data_list(cid,month):
    #https: // api.bilibili.com / x / v2 / dm / history / index?type = 1 & oid = 182435882 & month = 2020 - 04

    data_list_url = f'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={cid}&month={month}'
    res = requests.get(data_list_url,cookies=cookies)
    res_dict=json.loads(res.text)
    data_list=res_dict.get('data')
    return data_list
def _get_dan_mu_xml(cid,date):
    dan_mu_url = f'https://api.bilibili.com/x/v2/dm/history?type=1&oid={cid}&date={date}'
    res=requests.get(dan_mu_url,cookies=cookies)
    da_mu_xml=res.content.decode('utf8')
    #print(dan_mu_url)
    return da_mu_xml
def _parse_dan_mu(_get_dan_mu_xml):
    #print(_get_dan_mu_xml)
    reg=re.compile('<d p="([\s\S]*?)">([\s\S]+?)</d>')

    find_result=reg.findall(_get_dan_mu_xml)

    dan_mu_list=[]
    for line in find_result:
        p,dan_mu=line
        dm_time=float(p.split(',')[0])

        time_stamp = int(p.split(',')[4])
        dm_type = int(p.split(',')[5])
        dm_id=p.split(',')[6]
        date_array=datetime.datetime.fromtimestamp(time_stamp)
        send_time=date_array.strftime('%Y-%m-%d %H:%M:%S')
        dan_mu_list.append([dm_time,send_time,dm_type,dm_id,dan_mu])
    return dan_mu_list
def get_status(bv):
    transorform=AvBv()
    aid=transorform.dec(bv)
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av77413543',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    info = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
    info_rsp = requests.get(url=info, headers=headers)
    info_json = info_rsp.json()
    info_data=info_json['data']
    return info_data

def get_view(bvid):
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av77413543',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    info =' https://api.bilibili.com/x/web-interface/view?bvid='+ bvid
    info_rsp = requests.get(url=info, headers=headers)
    info_json = info_rsp.json()
    info_data=info_json['data']
    return info_data



class language:
    def __init__(self):
        str=''
        with open('Enlist.txt',encoding='UTF8') as f :
            str=f.read()
        self.Endict=json.loads(str)
        #self.status_En=Endict['status']
        #print(self.status_En)
    def status_ENtoCn(self,str):
        status_En = self.Endict['status']
        En=str

        CN=status_En[En]
        return CN


def getAllCommentList(bv):
    transorform=AvBv()
    av=transorform.dec(bv)
    url = "http://api.bilibili.com/x/reply?type=1&oid=" + str(av) + "&pn=1&nohot=1&sort=0"
    info_list=[]
    filename=f'{bv}/{bv}_comment.csv'
    r = requests.get(url)
    numtext = r.text
    json_text = json.loads(numtext)
    commentsNum = json_text["data"]["page"]["count"]
    page = commentsNum // 20 + 1
    #page=2
    for n in tqdm(range(1, page)):
        url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=" + str(n) + "&type=1&oid=" + str(av) + "&sort=1&nohot=1"
        req = requests.get(url)
        text = req.text
        json_text_list = json.loads(text)
        # for i in json_text_list["data"]["replies"]:
        #     #print([i["member"]["uname"], i["content"]["message"]])
        #     info_list.append([i["member"]["uname"], i["content"]["message"],i['like']])
        get_replies(json_text_list["data"],info_list,n)
        #info_list.append(json_text_list)
    tmp_df=pd.DataFrame(info_list,columns=['uname','sex','message','like','rpid','root','ctime','page'])
    tmp_df.to_csv(filename,index=False)
    return info_list


def get_replies(data,info_list,page):
    n=page
    if data['replies']==None:
        return
    else:
        for replies in data['replies']:
            info_list.append([replies["member"]["uname"],replies["member"]["sex"], replies["content"]["message"], replies['like'],replies['rpid'],replies['root'],replies['ctime'],n])
            get_replies(replies, info_list,n)

# def get_replies(data,info_list):
#     for replies in data['replies']:
#         info_list.append([replies["member"]["uname"], replies["content"]["message"], replies['like'],replies['rpid'],replies['root'],replies['ctime']])
#         get_replies(replies, info_list)


def get_data_history(cid_data_list,pubdate,nowdate):
    date_history_list=[]

    for cid_item in cid_data_list:
        # print(time.strftime("%Y--%m--%d %H:%M:%S", pudtime))
        # print(time.strftime("%Y--%m--%d %H:%M:%S", now))
        #now = datetime.date.today()
        now= datetime.datetime.now()
        #nowdate=time.time()
        #now=time.localtime(nowdate)
        pudtime =datetime.datetime.fromtimestamp(pubdate)
        year = now.year
        month = now.month
        #print(now)
        start_year = pudtime.year
        start_mounth = pudtime.month
        #pre_month_last_day = now.date()
        pre_month_last_day = now.date()
        while pre_month_last_day>pudtime.date():
            one_month_date_list = _get__one_month_data_list(cid_item['cid'],f'{year}-{month:>02}')
            print(one_month_date_list)
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


def get_all_dan_mu(data_historry_list,bv):
    for item in data_historry_list:
        part_name = item.get('part_name')
        filename = bv
        if part_name:
            filename=f'{bv}_{part_name}'
        with open(f'{filename}.txt','w',encoding='utf8') as f:
            for date in tqdm(item['date_list']):
                dan_mu_xml=_get_dan_mu_xml(item['cid'],date)
                dan_mu_list=_parse_dan_mu(dan_mu_xml)
                #print(dan_mu_list[0])
                for dan_mu_item in dan_mu_list:
                    line = '<;>'.join(dan_mu_item)
                    f.writelines(line)
                    f.write('\n')

def get_all_dan_mu_new(data_historry_list,bv):
    for item in data_historry_list:
        #print(item)
        part_name = item.get('part_name')
        part_name=part_name.replace('.','_')
        filename = bv
        all_dm_list=[]
        if part_name:
            filename=f'{bv}_{part_name}.csv'
        #with open(f'{filename}.txt','w',encoding='utf8') as f:
        for date in tqdm(item['date_list']):
            dan_mu_xml=_get_dan_mu_xml(item['cid'],date)
            dan_mu_list=_parse_dan_mu(dan_mu_xml)
            all_dm_list.extend(dan_mu_list)
            #print(dan_mu_list[0])
            # for dan_mu_item in dan_mu_list:
            #     line = '<;>'.join(dan_mu_item)
            #     f.writelines(line)
         #     f.write('\n')
        df=pd.DataFrame(all_dm_list,columns=['time','sendtime','dmtype','id','content'])
        df.to_csv(f'{bv}/{filename}', index=False)

if __name__ == '__main__':
    a=language()

    bv="BV1VD4y1D788"
    #bv='BV1w64y1c7Gb'
    dirs=f'{bv}'
    if not os.path.exists(dirs):
        os.makedirs(f'{dirs}')

    cookie_str="""CURRENT_FNVAL=16; _uuid=38285B20-6C3C-34A8-744A-B823DDF01C2C48839infoc; buvid3=2978B47B-C905-47F9-8D8A-4AC344F02378155816infoc; DedeUserID=4348911; DedeUserID__ckMd5=6ace9c7a6f620f59; SESSDATA=9b4d7c1a%2C1607260982%2C844d4*61; bili_jct=a6fbb288df0ecb23bb10c8d57664e0e5; LIVE_BUVID=AUTO5815917089829153; rpdid=|(k)~u~)lmmY0J'ulmkm|JJ)Y; PVID=4; sid=5suetco3"""
    cookies = format_cookie(cookie_str)
    cid_data_list=get_cid(bv)
    view=get_view(bv)
    print(view)
    aid=view['stat']['aid']
    pubdate=view['pubdate']
    now_date=view['ctime']
    name=view['title']
    #get_aid(cid_data_list[0]['cid'])
    #aid,start_day=get_startday(bv)
    data_historry_list=get_data_history(cid_data_list,pubdate,now_date)
    print(data_historry_list)
    # view=getAllCommentList(bv)
    # print(view)
    #print(data_historry_list)
    getAllCommentList(bv)
    get_all_dan_mu_new(data_historry_list,bv)