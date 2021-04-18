from flask_restful import Api
from .import videoPage
from .view import *

# 将 user 模块蓝图加入Api进行管理
api = Api(videoPage)

# 进行路由分发，类似于Django中的url工作内容（视图处理类， 请求路径）
api.add_resource(getVideoInfo, '/web-interface/view')
api.add_resource(getRecommend, '/web-interface/archive/related')
api.add_resource(getComment, '/v2/reply/main')
api.add_resource(getTags, '/tag/archive/tags')
api.add_resource(getVideoDownUrl, '/videoDownload')
api.add_resource(getVideoDataInfo, '/videodatainfo')