from flask_restful import Api
from .import mainPage
from .view import *
# 将 user 模块蓝图加入Api进行管理
api = Api(mainPage)

# 进行路由分发，类似于Django中的url工作内容（视图处理类， 请求路径）
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



    