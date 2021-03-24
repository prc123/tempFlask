from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderBiliView import *
from app.dmscripy.spider.spiderBiliChannle import *
from flask_cors import CORS
import json
# from app.api.bilibili_api.channel import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)



@app.route('/')
def hello_world():
   return 'Hello World'

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


api.add_resource(getBannerApi, '/banner')
api.add_resource(getDingApi, '/ding')

# api.add_resource(getPromote, '/promote')
api.add_resource(getPromote, '/promote')
# api.add_resource(contentRank, '/contentrank/')
api.add_resource(contentRankList, '/contentrank')
api.add_resource(contentRankWeek, '/contentrankweek')
api.add_resource(getRecommend, '/ranking3')
api.add_resource(live, '/live')
api.add_resource(channleDynamic, '/region')
api.add_resource(channleRank, '/regionrank')

# api.add_resource(contentRankWeek, '/ranking3')
if __name__ == '__main__':

   # print(a)
   # print(b)
   app.run(port=9050,debug=True)

