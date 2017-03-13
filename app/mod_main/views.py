from app import mongo_utils, mongo,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util, ObjectId
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash,session
from flask.ext.security import login_required, current_user
import os, json
from slugify import slugify
from werkzeug.utils import secure_filename
import time
from datetime import datetime

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def index():
    docs = mongo_utils.find_all()
    questions=mongo_utils.find_all_questions()
    count_questions=mongo_utils.get_nr_questions()
    return render_template('mod_main/index.html',docs=json.loads(json_util.dumps(docs)),questions=json.loads(json_util.dumps(questions)),count_questions=count_questions)

@mod_main.route('/insertuseranswers', methods=['GET', "POST"])
def insert_user_answers():
    if request.method == 'POST':
        timestamp=""
        user_id=""
        if session['user_id']=="":
            timestamp = int(time.mktime(datetime.now().timetuple()))
            session['user_id'] = timestamp
            user_id=session['user_id']
        else:
            user_id=session['user_id']

        data = request.form.to_dict()
        data['user_id']=user_id
        result=mongo_utils.insert_users_answers(data)
    #return render_template('mod_main/user_candidate_results.html.html', docs=json.loads(json_util.dumps(docs)), questions=json.loads(json_util.dumps(questions)), count_questions=count_questions)
    return Response(response=json_util.dumps(result), status=200, mimetype='application/json')