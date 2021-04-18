from flask import Flask, request,make_response,jsonify
from flask_restful import reqparse, abort, Api, Resource
# from app.dmscripy.spider.spiderClass import *
from app.dmscripy.spider.spiderVideoinfo import *
from app.api.userinfo import userinfo
import json



class getCookies(Resource):
      def get(self):
            pass 
      def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str)
        args=parser.parse_args()
        user=userinfo.userinfo()
        ##验证post请求token设置返回token，须加自定义头给前端解析
        ret,token=user.setCookies(args['value'])
        res=make_response(jsonify(ret))
        res.headers['token']=token
        res.headers['Access-Control-Expose-Headers']="token"
        return res

