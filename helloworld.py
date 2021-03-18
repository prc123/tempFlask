from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderBiliView import *
from flask_cors import CORS
import json

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

api.add_resource(getBannerApi, '/banner')
api.add_resource(getDingApi, '/ding')

# api.add_resource(getPromote, '/promote')
api.add_resource(getPromote, '/promote')
# api.add_resource(contentRank, '/contentrank/')
api.add_resource(contentRankList, '/contentrank')
api.add_resource(contentRankWeek, '/contentrankweek')
api.add_resource(getRecommend, '/ranking3')
api.add_resource(live, '/live')
# api.add_resource(contentRankWeek, '/ranking3')
if __name__ == '__main__':
   # print(spiderBiliView.getWebLive())
   app.run(port=9050,debug=True)

