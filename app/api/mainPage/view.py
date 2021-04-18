from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderBiliView import *
from app.dmscripy.spider.spiderBiliChannle import *
import json
class getDingApi(Resource):
      def get(self):
         return spiderBiliView.getDing()

class getBannerApi(Resource):
      def get(self):
         return spiderBiliView.getbanner()
class getPromote(Resource):
      def get(self):
         return spiderBiliView.getPromote()


class contentRank(Resource):
       def get(self):
            return spiderBiliView.getContenRank()

class contentRankList(Resource):
       def post(self):
            # args = parser.parse_args()
            date = json.loads(request.get_data(as_text=True))
            return spiderBiliView.getContenRankList(date["categoryId"])
class contentRankWeek(Resource):
       def post(self):
            # args = parser.parse_args()
            date = json.loads(request.get_data(as_text=True))
            return spiderBiliView.getContenRankWeek(date["categoryId"])

class getRecommend(Resource):
       def get(self):
              return spiderBiliView.getRecommend()


class live(Resource):
      def get(self):
         return spiderBiliView.getWebLive()

class channleDynamic(Resource):
      def get(self):
         # date = json.loads(request.get_data(as_text=True))
         rid=request.args.get("rid")
         ps=request.args.get("ps")
         return spiderBiliChannle.getChannleDynamic(rid,ps)

class channleRank(Resource):
      def get(self):
         # date = json.loads(request.get_data(as_text=True))
         rid=int(request.args.get("rid"))
         day=int(request.args.get("day"))
         return spiderBiliChannle.getChannleRank(rid,day)

