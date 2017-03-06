from flask import Blueprint, render_template, url_for, request
from bson.json_util import dumps

mod_whatis = Blueprint('whatis', __name__, url_prefix='/whatis')
@mod_whatis.route('/', methods=['GET'])
def index():
    return render_template('mod_whatis/index.html')
