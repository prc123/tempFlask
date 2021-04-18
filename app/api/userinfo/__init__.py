from flask import Blueprint
user = Blueprint('user', __name__,url_prefix="/user/")
# from flask_cors import CORS
# CORS(user)
from . import urls