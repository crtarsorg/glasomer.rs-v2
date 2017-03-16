from app import mongo_utils, mongo,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util, ObjectId
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash
from flask.ext.security import login_required, current_user
import os, json
from slugify import slugify
from werkzeug.utils import secure_filename
from flask.ext.security import current_user


mod_project = Blueprint('projects', __name__, url_prefix='/projects')
@mod_project.route('/', methods=['GET', "POST"])
def index():
    if current_user.is_authenticated:
        return render_template('mod_project/projects.html')
    else:
        return redirect(url_for('auth.login'))

@mod_project.route('/getallprojects', methods=['GET', "POST"])
def get_all_projects():
    docs = mongo_utils.find_all_projects()
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_project.route('/addproject', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.insert_project(data)
    flash('Project is saved')
    return redirect(url_for('projects.index'))

@mod_project.route('/editproject', methods=['GET', 'POST'])
def edit_project():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.update_project(data)
    flash('Project is saved')
    return redirect(url_for('projects.index'))

@mod_project.route('/getselectedproject', methods=['GET', 'POST'])
def get_selected_project():
    if request.method == 'POST':
        data = request.form.to_dict()
    docs = mongo_utils.find_selected_project(data)
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_project.route('/deleteproject', methods=['GET', "POST"])
def delete_project():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.remove_project(data)
        docs = mongo_utils.find_all_projects()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_project.route('/changestatus', methods=['GET', "POST"])
def change_status():
    if request.method == 'POST':
        data = request.form.to_dict()
        getstatus=mongo_utils.get_status(data)
        if getstatus['enabled']=="disabled":
            data['enabled']="enabled"
        else:
            data['enabled'] = "disabled"
        mongo_utils.edit_status(data)
        docs = mongo_utils.find_all_projects()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')
