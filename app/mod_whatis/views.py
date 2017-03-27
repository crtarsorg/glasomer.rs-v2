from flask import Blueprint, render_template, url_for, request
from bson.json_util import dumps
from app import mongo_utils
from bson import json_util, ObjectId
import os, json
mod_whatis = Blueprint('whatis', __name__, url_prefix='/sta-je-glasomer')
@mod_whatis.route('/', methods=['GET'])
def index():
    year = ""
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        year = project['year']
    glasomer_text = mongo_utils.find_glasomer_text(year)
    return render_template('mod_whatis/index.html',glasomer_text=json.loads(json_util.dumps(glasomer_text)))
