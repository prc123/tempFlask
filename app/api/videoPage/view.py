from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderVideoinfo import *
import json
class getVideoInfo(Resource):
        
      def get(self):
        print(request.args)

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
