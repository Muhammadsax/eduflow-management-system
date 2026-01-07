from flask import Blueprint

bp = Blueprint('auth', __name__)

from eduflow_app.auth import routes