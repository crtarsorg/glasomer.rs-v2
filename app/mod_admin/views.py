from app import mongo_utils, mongo,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util, ObjectId
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash
from flask.ext.security import login_required, current_user
import os, json
from slugify import slugify
from werkzeug.utils import secure_filename



mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/', methods=['GET', "POST"])
#@login_required
def index():
    return render_template('mod_admin/index.html')

@mod_admin.route('/candidates', methods=['GET', "POST"])
def candidates():
    return render_template('mod_admin/candidates.html')

@mod_admin.route('/getallcandidates', methods=['GET', 'POST'])
def get_all_candidates():
    docs = mongo_utils.find_all_candidates()
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@mod_admin.route('/addcandidate', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
        submitted_file = request.files['fileupload']
        filename=''
        if submitted_file.filename!='':
            filename = submitted_file.filename
            submitted_file.save(os.path.join(os.path.join(UPLOAD_FOLDER), filename))
        docs=mongo_utils.insert_candidate(data,filename)
    flash('Candidate is added')
    return redirect(url_for('admin.candidates'))

@mod_admin.route('/getselectedcandidate', methods=['GET', 'POST'])
def get_selected_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
    docs = mongo_utils.find_selected_candidate(data)
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/addgroup', methods=['GET', "POST"])
def insert_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.insert_question(data)
        docs = mongo_utils.find_all()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/editcandidate', methods=['GET', "POST"])
def edit_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
        submitted_file = request.files['fileupload']
        filename=''
        if submitted_file.filename != '':
            filename = submitted_file.filename
            submitted_file.save(os.path.join(os.path.join(UPLOAD_FOLDER), filename))
        else:
            filename = data['image_hidden']
        mongo_utils.update_candidate(data, filename)
    flash('Candidate is edited')
    return redirect(url_for('admin.candidates'))

@mod_admin.route('/deletecandidate', methods=['GET', "POST"])
def delete_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.remove_candidate(data)
        docs = mongo_utils.find_all_candidates()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/getallquestions', methods=['GET', "POST"])
def get_all_groups():
    if request.method == 'GET':
        docs = mongo_utils.find_all()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/getnrgroups', methods=['GET', "POST"])
def get_nr_groups():
    if request.method == 'GET':
        docs = mongo_utils.count_groups()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')
@mod_admin.route('/getselectedgroup', methods=['GET', "POST"])
def get_selected_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs = mongo_utils.find_selected_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/editselectedgroup', methods=['GET', "POST"])
def edit_selected_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.update_selected_group(data)
        docs= mongo_utils.find_all()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/deletegroup', methods=['GET', "POST"])
def delete_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.remove_group(data)
        docs= mongo_utils.find_all()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')
@mod_admin.route('/getquestions', methods=['GET', "POST"])
def get_questions():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs= mongo_utils.find_questions(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/addquestiongroup', methods=['GET', "POST"])
def add_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.insert_question_group(data)
        docs = mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/getselectedquestion', methods=['GET', "POST"])
def get_selected_question():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs=mongo_utils.find_selected_question(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/editquestiongroup', methods=['GET', "POST"])
def edit_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.update_selected_question(data)
        docs= mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@mod_admin.route('/removequestion', methods=['GET', "POST"])
def remove_question():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.delete_question(data)
        docs= mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

#candidates answrs
@mod_admin.route('/answerscandidates', methods=['GET', "POST"])
def answers_candidates():
    candidate_url = request.args.get('candidate')
    docs = mongo_utils.find_all()
    questions=mongo_utils.find_all_questions()
    return render_template('mod_admin/answers_candidates.html',docs=json.loads(json_util.dumps(docs)),questions=json.loads(json_util.dumps(questions)),candidate_url=candidate_url)

@mod_admin.route('/addcandidateanswers', methods=['GET', "POST"])
def add_candidate_answers():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.insert_candidate_answers(data)
    return redirect(url_for('admin.candidates'))

@mod_admin.route('/getcandidateanswers', methods=['GET', "POST"])
def get_candidate_answers():
    candidate_url = request.args.get('candidate')
    questions=mongo_utils.find_all_questions()
    nr_questions=mongo_utils.get_nr_questions()
    candidate_answers=mongo_utils.get_candidate_asnwers(candidate_url)
    docs = mongo_utils.find_all()
    return render_template('mod_admin/answers_candidate_results.html',docs=json.loads(json_util.dumps(docs)), candidates=json.loads(json_util.dumps(candidate_answers)),questions=json.loads(json_util.dumps(questions)),nr_questions=json_util.dumps(nr_questions),candidate_url=candidate_url)

@mod_admin.route('/editcandidateanswers', methods=['GET', "POST"])
def edit_candidate_answers():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.update_candidate_answers(data)
    return redirect(url_for('admin.candidates'))
