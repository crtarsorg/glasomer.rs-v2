from app import mongo_utils,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash
from flask.ext.security import login_required
import os, json
from flask.ext.security import current_user

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/', methods=['GET', "POST"])
def index():
    if current_user.is_authenticated:
        projects = mongo_utils.find_all_projects()
        return render_template('mod_admin/index.html',projects=json.loads(json_util.dumps(projects)))
    else:
        return redirect(url_for('auth.login'))

@login_required
@mod_admin.route('/candidates', methods=['GET', "POST"])
def candidates():
    return render_template('mod_admin/candidates.html')

@login_required
@mod_admin.route('/getallcandidates', methods=['GET', 'POST'])
def get_all_candidates():
    docs = mongo_utils.find_all_candidates()
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@login_required
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


@login_required
@mod_admin.route('/getselectedcandidate', methods=['GET', 'POST'])
def get_selected_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
    docs = mongo_utils.find_selected_candidate(data)
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')


@login_required
@mod_admin.route('/addgroup', methods=['GET', "POST"])
def insert_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.insert_question(data)
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            docs = mongo_utils.find_all(project['year'])
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
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

@login_required
@mod_admin.route('/deletecandidate', methods=['GET', "POST"])
def delete_candidate():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.remove_candidate(data)
        docs = mongo_utils.find_all_candidates()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/getallquestions', methods=['GET', "POST"])
def get_all_groups():
    if request.method == 'GET':
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            docs = mongo_utils.find_all(project['year'])
        for doc in json.loads(json_util.dumps(docs)):
            result=mongo_utils.update_order_by_grop(doc)
        return Response(response=json_util.dumps(result), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/getnrgroups', methods=['GET', "POST"])
def get_nr_groups():
    if request.method == 'GET':
        docs = mongo_utils.count_groups()
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/getselectedgroup', methods=['GET', "POST"])
def get_selected_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs = mongo_utils.find_selected_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/editselectedgroup', methods=['GET', "POST"])
def edit_selected_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            docs = mongo_utils.find_all(project['year'])
            data['project_slug']=project['year']
        mongo_utils.update_selected_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/deletegroup', methods=['GET', "POST"])
def delete_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.remove_group(data)
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            docs = mongo_utils.find_all(project['year'])
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/getquestions', methods=['GET', "POST"])
def get_questions():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs= mongo_utils.find_questions(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/addquestiongroup', methods=['GET', "POST"])
def add_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        find_prject=mongo_utils.find_group_project(data['group_name'])
        for group in json.loads(json_util.dumps(find_prject)):
            data['project_slug']=group['project_slug']
        mongo_utils.insert_question_group(data)
        docs = mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/getselectedquestion', methods=['GET', "POST"])
def get_selected_question():
    if request.method == 'POST':
        data = request.form.to_dict()
        docs=mongo_utils.find_selected_question(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/editquestiongroup', methods=['GET', "POST"])
def edit_question_group():
    if request.method == 'POST':
        data = request.form.to_dict()
        find_prject = mongo_utils.find_group_project(data['group_name'])
        for group in json.loads(json_util.dumps(find_prject)):
            data['project_slug'] = group['project_slug']
        mongo_utils.update_selected_question(data)
        docs= mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/removequestion', methods=['GET', "POST"])
def remove_question():
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.delete_question(data)
        find_prject = mongo_utils.find_group_project(data['group_name'])
        for group in json.loads(json_util.dumps(find_prject)):
            data['project_slug'] = group['project_slug']
        docs= mongo_utils.find_question_group(data)
        return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

#candidates answrs
@login_required
@mod_admin.route('/answerscandidates', methods=['GET', "POST"])
def answers_candidates():
    candidate_url = request.args.get('candidate')
    project_enabled=mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        docs = mongo_utils.find_all(project['year'])
        questions=mongo_utils.find_all_questions(project['year'])
    for doc in json.loads(json_util.dumps(questions)):
        questions1=mongo_utils.update_order_by(doc)
    return render_template('mod_admin/answers_candidates.html',docs=json.loads(json_util.dumps(docs)),questions=json.loads(json_util.dumps(questions1)),candidate_url=candidate_url)

@login_required
@mod_admin.route('/addcandidateanswers', methods=['GET', "POST"])
def add_candidate_answers():
    if request.method == 'POST':
        data = request.form.to_dict()
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            data['project_slug']=project['year']
        mongo_utils.insert_candidate_answers(data)
    return redirect(url_for('admin.candidates'))

@login_required
@mod_admin.route('/getcandidateanswers', methods=['GET', "POST"])
def get_candidate_answers():
    candidate_url = request.args.get('candidate')

    nr_questions=mongo_utils.get_nr_questions()
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        questions = mongo_utils.find_all_questions(project['year'])
        docs = mongo_utils.find_all(project['year'])
        candidate_answers=mongo_utils.get_candidate_asnwers(candidate_url,project['year'])

    return render_template('mod_admin/answers_candidate_results.html',docs=json.loads(json_util.dumps(docs)), candidates=json.loads(json_util.dumps(candidate_answers)),questions=json.loads(json_util.dumps(questions)),nr_questions=json_util.dumps(nr_questions),candidate_url=candidate_url)

@login_required
@mod_admin.route('/editcandidateanswers', methods=['GET', "POST"])
def edit_candidate_answers():
    if request.method == 'POST':
        data = request.form.to_dict()
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            data['project_slug']=project['year']
        mongo_utils.update_candidate_answers(data)
    return redirect(url_for('admin.candidates'))

@login_required
@mod_admin.route('/updateordergroup', methods=['GET', "POST"])
def update_order_group():
    if request.method == 'POST':
        data= request.form.to_dict()
        json_data = None
        for element in data:
            json_data = json.loads(element)
        mongo_utils.update_order(json_data)
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        docs = mongo_utils.find_all(project['year'])

    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/updateorderquestion', methods=['GET', "POST"])
def update_order_question():
    if request.method == 'POST':
        data= request.form.to_dict()
    json_data = None
    for element in data:
        json_data = json.loads(element)
    mongo_utils.update_order_questions(json_data)
    for element in data:
        json_data = json.loads(element)
    docs = mongo_utils.find_question_group_ordered(json_data)
    return Response(response=json_util.dumps(docs), status=200, mimetype='application/json')

@login_required
@mod_admin.route('/glasomer/manage-sta-je-glasomer', methods=['GET', "POST"])
def whatisglasomer():
    year=""
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        year = project['year']
    glasomer_text=mongo_utils.find_glasomer_text(year)
    return render_template('mod_admin/whatisglasomer.html',glasomer_text=json.loads(json_util.dumps(glasomer_text)))


@mod_admin.route('/glasomer/saveglasomertext', methods=['GET', 'POST'])
def save_glasomer_text():
    year=""
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        year =project['year']
    if request.method == 'POST':
        data = request.form.to_dict()
        mongo_utils.delete_glasomer_text(year)
        mongo_utils.edit_glasomer_text(data,year)
        flash('Text is saved')
    return redirect(url_for('admin.whatisglasomer'))