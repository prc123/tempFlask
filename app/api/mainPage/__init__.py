from flask import Blueprint

mainPage = Blueprint('mainPage', __name__,url_prefix="/")

from . import urls