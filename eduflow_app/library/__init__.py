from flask import Blueprint

bp = Blueprint('library', __name__)

# سنستورد المسارات لاحقاً
from eduflow_app.library import routes