from flask import Flask, request,Response,stream_with_context,jsonify

from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderVideoinfo import *
from app.api.userinfo.userinfo import userinfo
from app.utils.dmparse import dmparse
import json
import time
import datetime
from wordcloud import WordCloud
import base64
from io import BytesIO

class getVideoInfo(Resource):
      def get(self):
        arg = request.args.get("bvid")
        return spiderVideoinfo.getVideoInfo(bvid=arg)

class getRecommend(Resource):
      def get(self):

        arg = request.args.get("bvid")
        return spiderVideoinfo.getRelated(bvid=arg)

class getComment(Resource):
      def get(self):
        arg = request.args.get("bvid")
        return spiderVideoinfo.getCommentsG(bvid=arg)

class getTags(Resource):
      def get(self):
        arg = request.args.get("bvid")
        return spiderVideoinfo.getTags(bvid=arg)

class getVideoDownUrl(Resource):
      def get(self):
          arg = request.args.get("bvid")
          return spiderVideoinfo.getVideoUrl(bvid=arg)

class getVideoDataInfo(Resource):
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
      def get(self):    
            parser = reqparse.RequestParser()
            parser.add_argument('token', type=str,location="headers")
            parser.add_argument('date', type=str)
            parser.add_argument('oid', type=int)
            args=parser.parse_args()
            user=userinfo()
            bv = request.args.get("bvid")
            infoType=request.args.get("type")
            date=args.get("date")
            token=args.get("token")
            oid=args.get("oid")

            if infoType =="dm":
                  if user.verifyToken(token)==False:
                        return {'code':-1,'message':"token验证失败"},403
                  _,v=user.verifyCookies(user.cookies)    
                  res={"time":date , "dmtime":{},"wordtimes":{}}
                  date=datetime.datetime.strptime(date,"%Y-%m-%d")  
                  dmInfo=spiderVideoinfo.getVideoDm(bvid=bv,date=date,oid=oid,verify=v)
                  groupdm=dmInfo.groupby("time").count()['id']
                  res['dmtime']['index']=groupdm.index.tolist()
                  res['dmtime']['times']=groupdm.values.tolist()
                  wordDict=dmparse.getDmWordTimesNoWordCut(dmInfo, "content")
                  # wordDict=dmparse.getDmWordTimes(dmInfo, "content")
                  wordDict=wordDict[0:200]
                  res['wordtimes']['word']=wordDict['id'].values.tolist()
                  res['wordtimes']['times']=wordDict['times'].values.tolist()
                  str1=" ".join(res['wordtimes']['word'])
                  
                  wordcloud = WordCloud(font_path='simfang.ttf',width=400,height=500,background_color="white",font_step=1,relative_scaling=0,max_font_size=60).generate(str1)
                  dmcloud=wordcloud.to_image()
                  bImg = BytesIO()
                  dmcloud.save(bImg, format='jpeg')
                  bImg = bImg.getvalue()
                  b64Img = base64.b64encode(bImg)
                  res['dmtime']['dmcloud']=b64Img.decode("ascii")
                  # print(base64.b64encode(dmcloud))
                  # Display the generated image:
                  # the matplotlib way:
                  # import matplotlib.pyplot as plt
                  # plt.imshow(wordcloud, interpolation='bilinear')
                  # plt.axis("off")
                  # plt.show()
                  return jsonify(res)
            elif infoType =="cmt":
                  pass
            else:
                  pass
         
                  

