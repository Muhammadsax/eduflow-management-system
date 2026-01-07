from flask import Blueprint

bp = Blueprint('main', __name__)

from eduflow_app.main import routes