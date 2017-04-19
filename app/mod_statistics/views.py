from app import mongo_utils,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash
from flask.ext.security import login_required
import os, json
from flask.ext.security import current_user

mod_statistics = Blueprint('statistics', __name__, url_prefix='/statistics')

@mod_statistics.route('/', methods=['GET', "POST"])
def index():
    year = ""
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        year = project['year']
    visited_users = mongo_utils.count_visits(year)
    count_voters=0
    result_voters=mongo_utils.get_voters_count(year)
    for c_v in result_voters:
        print c_v
    return render_template('mod_statistics/index.html',visited_users=visited_users,voters=len(result_voters))

