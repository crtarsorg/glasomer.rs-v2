# coding=utf-8
import pprint
from app import mongo_utils, mongo,UPLOAD_FOLDER,ALLOWED_EXTENSIONS
from bson import json_util, ObjectId
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash,session
import os, json
import time
from datetime import datetime
from flask.ext.security import current_user

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET'])
def index():
    project_enabled = mongo_utils.get_enabled_project()
    for project in json.loads(json_util.dumps(project_enabled)):
        docs = mongo_utils.find_all(project['year'])
        count_questions = mongo_utils.get_nr_questions_front(project['year'])
        questions = mongo_utils.find_all_questions(project['year'])
    return render_template('mod_main/index.html', docs=json.loads(json_util.dumps(docs)),questions=json.loads(json_util.dumps(questions)), count_questions=count_questions)


@mod_main.route('/insertuseranswers', methods=['GET', "POST"])
def insert_user_answers():
    if request.method == 'POST':
        if session.get('user_id') is not None:
            user_id=session['user_id']

        else:
            timestamp = int(time.mktime(datetime.now().timetuple()))
            session['user_id'] = timestamp
            user_id = session['user_id']
        data = request.form.to_dict()
        project_enabled = mongo_utils.get_enabled_project()

        for project in json.loads(json_util.dumps(project_enabled)):
            docs = mongo_utils.find_all(project['year'])
            data['project_slug']=project['year']

        data['user_id'] = user_id
        data['timestamp'] = datetime.datetime.utcnow()
        result=mongo_utils.insert_users_answers(data)
    #return render_template('mod_main/user_candidate_results.html.html', docs=json.loads(json_util.dumps(docs)), questions=json.loads(json_util.dumps(questions)), count_questions=count_questions)
    return Response(response=json_util.dumps(result), status=200, mimetype='application/json')

@mod_main.route('/getallquestions', methods=['GET', "POST"])
def get_all_questions():
    if request.method == 'GET':
        array_questions=[]
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            groups=mongo_utils.find_all(project['year'])

        for group in json.loads(json_util.dumps(groups)):
            questions = mongo_utils.find_all_questions_ordered(group['generated_id'])
            for question in questions:
                array_questions.append(question)

    return Response(response=json_util.dumps(array_questions), status=200, mimetype='application/json')

@mod_main.route('/getquestionsresults', methods=['GET', "POST"])
def get_questions_results():
    if request.method == 'POST':
        user_id=session['user_id']
        data = request.form.to_dict()
        question= data['question_name']
        project_slug=""
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            project_slug=project['year']
            questions = mongo_utils.find_all_questions(project['year'])
            response = mongo_utils.find_all_questions_results(user_id,question,project['year'])
        count_question=0
        created_array = []
        question_key=""
        for questions in json.loads(json_util.dumps(response['all_question'])):
            count_question = count_question + 1
            question_key=count_question
            answers = mongo_utils.find_all_answers_s(question_key,question,project_slug)
            answers_users = mongo_utils.find_all_answers_users(question_key,question,user_id,project_slug)
            for r in json.loads(json_util.dumps(answers)):
                candidate_name_result = mongo_utils.get_candidate_name(r['candidate_slug'])
                for c_name in json.loads(json_util.dumps(candidate_name_result)):
                    candidate_name=c_name['candidate_name']
                    if 'status_'+str(question_key) in r:
                        status=r['status_'+str(question_key)]
                    else:
                        status="/"
                    if 'vazno_'+str(question_key) in r:
                        vazno=r['vazno_'+str(question_key)]
                    else:
                        vazno="/"
                    if 'comment_' + str(question_key) in r:
                        comment = r['comment_' + str(question_key)]
                    else:
                        comment = "/"
                    created_array.append({'candidate_slug':candidate_name,'status':status,'vazno':vazno,'comment':comment})
            for r_u in json.loads(json_util.dumps(answers_users)):
                if 'status_' + str(question_key) in r_u:
                    status = r_u['status_' + str(question_key)]
                else:
                    status = "/"
                if 'vazno_' + str(question_key) in r_u:
                    vazno = r_u['vazno_' + str(question_key)]
                else:
                    vazno = "/"
                created_array.append({'candidate_slug': 'Vaš odgovor', 'status': status, 'vazno': vazno,'comment': "/"})
        return Response(response=json_util.dumps(created_array), status=200, mimetype='application/json')

@mod_main.route('/getallqu', methods=['GET', "POST"])
def get_all_q_a_u():
    if request.method == 'GET':
        if session.get('user_id') is not None:
            user_id = session['user_id']
        count_question=0
        create_question_array=[]
        project_slug=""
        project_enabled = mongo_utils.get_enabled_project()
        for project in json.loads(json_util.dumps(project_enabled)):
            response_all_questions=mongo_utils.find_all_questions(project['year'])
            project_slug=project['year']

        for raq in json.loads(json_util.dumps(response_all_questions)):
            count_question=count_question+1
            question_key=count_question
            response_user_q = mongo_utils.find_all_questions_user(user_id,project_slug)
            for ruq in json.loads(json_util.dumps(response_user_q)):
                if 'vazno_'+str(count_question) in ruq and 'status_'+str(count_question) in ruq:
                    create_question_array.append({'question_name':ruq['question_'+str(count_question)]})

        return Response(response=json_util.dumps(create_question_array), status=200, mimetype='application/json')

@mod_main.route('/getanswersusercandidate', methods=['GET', "POST"])
def get_answers_user_candidate():
    if request.method=="POST":
        if session.get('user_id') is not None:
            user_id = session['user_id']
        data = request.form.to_dict()
    created_array=[]
    count_question = 0
    question_key=0;
    response_users_questtion = mongo_utils.find_users_question_a(user_id)
    response_all_questions = mongo_utils.find_all_questions()
    for raq in json.loads(json_util.dumps(response_all_questions)):
        count_question = count_question + 1
        question_key=count_question
        response_canidates_questtion = mongo_utils.find_candidates_question_a(question_key,data['question_name'])
        answers_users = mongo_utils.find_all_answers_users(question_key, data['question_name'], user_id)
        for r_candidates in json.loads(json_util.dumps(response_canidates_questtion)):
            candidate_name_result = mongo_utils.get_candidate_name(r_candidates['candidate_slug'])
            for c_name in json.loads(json_util.dumps(candidate_name_result)):
                candidate_name = c_name['candidate_name']
            if 'status_' + str(question_key) in r_candidates:
                status = r_candidates['status_' + str(question_key)]
            else:
                status = "/"
            if 'vazno_' + str(question_key) in r_candidates:
                vazno = r_candidates['vazno_' + str(question_key)]
            else:
                vazno = "/"
            if 'comment_' + str(question_key) in r_candidates:
                comment = r_candidates['comment_' + str(question_key)]
            else:
                comment = "/"
            created_array.append({'candidate_slug':candidate_name,'vazno':vazno,'status':status,'comment':comment})

        for r_users in json.loads(json_util.dumps(answers_users)):
            if 'status_' + str(question_key) in r_users:
                status = r_users['status_' + str(question_key)]
            else:
                status = "/"
            if 'vazno_' + str(question_key) in r_users:
                vazno = r_users['vazno_' + str(question_key)]
            else:
                vazno = "/"
            created_array.append({'candidate_slug':"Vaš odgovor",'vazno':vazno,'status':status,'comment':"/"})
        return Response(response=json_util.dumps(created_array), status=200, mimetype='application/json')

