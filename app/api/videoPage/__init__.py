from flask import Blueprint
videoPage = Blueprint('videoPage', __name__,url_prefix="/x")

from . import urls