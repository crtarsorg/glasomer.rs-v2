from slugify import slugify
from bson import json_util
import time
from datetime import datetime
class MongoUtils(object):


    def __init__(self, mongo):
        self.mongo = mongo
        self.group_collection = "group_collection"
        self.questions_collection = "questions_collection"
        self.candidates_collection = "candidates_collection"
        self.answers_candidates = "answers_candidates"
        self.answers_users = "answers_users"
        self.projects_collection = "projects_collection"
        self.glasomer_text_collection = "glasomer_text_collection"
        self.visited_users = "visited_users"

    def insert_question(self, doc):
        count_groups=int(time.mktime(datetime.now().timetuple()))
        count_group=self.mongo.db[self.group_collection].count();
        result = self.mongo.db[self.group_collection].insert({'generated_id':str(count_groups)+"-"+slugify(doc['group_name']),'slug': slugify(doc['group_name']), 'group_name': doc['group_name'],'order_number':int(count_group+1),'project_slug':doc['project_slug']})
        return result


    def find_group(self, slug):
        result = self.mongo.db[self.group_collection].find_one({'slug': slug})
        return result

    def find_all(self,project_slug):
        result = self.mongo.db[self.group_collection].find({'project_slug':project_slug}).sort('order_number',1)
        return result

    def find_all_questions(self,project_slug):
        result = self.mongo.db[self.questions_collection].find({'project_slug':project_slug}).sort('order_number',1)
        return result

    def find_all_questions_ordered(self, group_slug):
        result = self.mongo.db[self.questions_collection].find({'group_slug': group_slug}).sort('order_number', 1)
        return result

    def update_order_by_grop(self,doc):
        result = self.mongo.db[self.group_collection].find({'project_slug': doc['project_slug']}).sort('order_number')
        return result

    def update_order_by(self,doc):
        self.mongo.db[self.questions_collection].update({'question_slug': doc['question_slug']},{'$set': {'order_number': int(doc['order_number'])}},multi=True)
        result = self.mongo.db[self.questions_collection].find({'project_slug': doc['project_slug']}).sort('order_number')
        return result

    def count_groups(self):
        result = self.mongo.db[self.group_collection].count()
        return result

    def count_visits(self,project_enabled):
        result = self.mongo.db[self.visited_users].count()
        return result

    def find_selected_group(self,doc):
        result = self.mongo.db[self.group_collection].find_one({'generated_id':doc['group_name']})
        return result

    def update_selected_group(self,doc):
        result = self.mongo.db[self.group_collection].update({'generated_id': doc['hidden_group']},{'$set': {'group_name': doc['group_name']}})
        return result

    def remove_group(self,doc):
        self.mongo.db[self.questions_collection].remove({'group_slug':doc['group_name']})
        result = self.mongo.db[self.group_collection].remove({'generated_id': slugify(doc['group_name'])})
        return result

    def find_questions(self, doc):
        result = self.mongo.db[self.questions_collection].find({'group_slug': doc['group_name']})
        return result

    def insert_question_group(self, doc):
        question_name=doc['question_name']
        count_group = self.mongo.db[self.questions_collection].find({'group_slug':doc['group_name']}).count()
        self.mongo.db[self.questions_collection].insert({'group_slug': doc['group_name'],"question_name" :question_name,'question_slug':slugify(question_name),'order_number':int(count_group+1),'project_slug':doc['project_slug']})
        result = self.mongo.db[self.group_collection].find()
        return result


    def find_selected_question(self, doc):
        result=self.mongo.db[self.questions_collection].find({'question_slug': doc['question_slug']})
        return result

    def update_selected_question(self, doc):

        result = self.mongo.db[self.questions_collection].update({'question_slug':doc['hidden_question']},
                                                                {'$set': {'question_name': doc['question_name']}})
        return result

    def find_question_group(self, doc):
        result = self.mongo.db[self.questions_collection].find({'group_slug': doc['group_name'],'project_slug':doc['project_slug']})
        return result

    def delete_question(self,doc):
        result = self.mongo.db[self.questions_collection].remove({'question_slug': slugify(doc['question_slug'])})
        return result


    def insert_candidate(self, doc, filename):
        count_groups=int(time.mktime(datetime.now().timetuple()))
        result = self.mongo.db[self.candidates_collection].insert({
                                                        'generated_id':str(count_groups)+"-"+slugify(doc['candidate_name']),
                                                        'slug': slugify(doc['candidate_name']),
                                                        'candidate_name': doc['candidate_name'],
                                                        'candidate_biography': doc['candidate_biography'],
                                                        'image': filename})
        return result
    def update_candidate(self, doc,filename):
        result = self.mongo.db[self.candidates_collection].update(
                                                        {'generated_id':doc['generated_id']},
                                                        {'generated_id': doc['generated_id'],
                                                        'slug': slugify(doc['candidate_name']),
                                                        'candidate_name': doc['candidate_name'],
                                                        'candidate_biography': doc['candidate_biography'],
                                                        'image': filename})
        return result

    def find_all_candidates(self):
        result = self.mongo.db[self.candidates_collection].find()
        return result

    def find_selected_candidate(self,doc):
        result = self.mongo.db[self.candidates_collection].find_one({'generated_id':doc['candidate_gid']})
        return result

    def remove_candidate(self,doc):
        result = self.mongo.db[self.candidates_collection].remove({'generated_id': doc['candidate_gid']})
        return result

    def insert_candidate_answers(self, doc):
        result = self.mongo.db[self.answers_candidates].insert(doc)

    def update_candidate_answers(self, doc):

        self.mongo.db[self.answers_candidates].remove({'candidate_slug': doc['candidate_slug'],'project_slug':doc['project_slug']})
        result = self.mongo.db[self.answers_candidates].insert(doc)
        return result

    def get_candidate_asnwers(self,candidate_url,project_slug):
        result = self.mongo.db[self.answers_candidates].find({'candidate_slug':candidate_url,'project_slug':project_slug})
        return result

    def get_nr_questions(self):
        result = self.mongo.db[self.questions_collection].count()
        return result

    def get_nr_questions_front(self, project_slug):
        result = self.mongo.db[self.questions_collection].find({'project_slug': project_slug}).count()
        return result

    def insert_users_answers(self, doc):
        self.mongo.db[self.answers_users].remove({'user_id': doc['user_id'],'project_slug':doc['project_slug']})
        self.mongo.db[self.answers_users].insert(doc)
        result_candidates=self.mongo.db[self.answers_candidates].find({'project_slug':doc['project_slug']})
        result_user=self.mongo.db[self.answers_users].find({'user_id':doc['user_id'],'project_slug':doc['project_slug']})
        candidates=self.mongo.db[self.candidates_collection].find()
        all_question=self.mongo.db[self.questions_collection].find({'project_slug':doc['project_slug']})

        return {'user_results':result_user, 'candidate_results':result_candidates,'candidates':candidates,'all_question':all_question}

    def find_user_session_answers(self, project_slug,user_id):
        result_candidates=self.mongo.db[self.answers_candidates].find({'project_slug':project_slug})
        result_user=self.mongo.db[self.answers_users].find({'user_id':int(user_id),'project_slug':project_slug})
        candidates=self.mongo.db[self.candidates_collection].find()
        all_question=self.mongo.db[self.questions_collection].find({'project_slug':project_slug})
        return {'user_results':result_user, 'candidate_results':result_candidates,'candidates':candidates,'all_question':all_question}


    def find_all_questions_results(self, user_id,question,project_slug):
        result_candidates=self.mongo.db[self.answers_candidates].find({'project_slug':project_slug})
        result_user = self.mongo.db[self.answers_users].find({'user_id':user_id,'project_slug':project_slug})
        all_question=self.mongo.db[self.questions_collection].find({'project_slug':project_slug}).sort('order_number')
        candidates = self.mongo.db[self.candidates_collection].find()
        return {'user_results':result_user, 'candidate_results':result_candidates,'candidates':candidates,'all_question':all_question}

    def find_all_answers_s(self,question_key,question,project_slug):
        result_candidates = self.mongo.db[self.answers_candidates].find({'question_'+str(question_key):question,'project_slug':project_slug})
        return result_candidates

    def get_candidate_name(self,candidate_slug):
        result_candidates_name = self.mongo.db[self.candidates_collection].find({'generated_id':candidate_slug})
        return result_candidates_name

    def find_all_questions_user(self,user_id,project_slug):
        result = self.mongo.db[self.answers_users].find({'user_id':int(user_id),'project_slug':project_slug})
        return result

    def find_all_questions_user_key(self,question_key):
        result = self.mongo.db[self.answers_users].find({'question_'+str(question_key): question_key})
        return result

    def find_candidates_question_a(self,question_key,question_name):
        result = self.mongo.db[self.answers_candidates].find({'question_'+str(question_key):question_name})
        return result

    def find_users_question_a(self,user_id):
        result = self.mongo.db[self.answers_users].find({'user_id':user_id})
        return result

    def find_all_answers_users(self,question_key,question,user_id,project_slug):
        result_candidates = self.mongo.db[self.answers_users].find({'question_'+str(question_key):question,'user_id':int(user_id),'project_slug':project_slug})
        return result_candidates

    def find_all_projects(self):
        result = self.mongo.db[self.projects_collection].find()
        return result

    def insert_project(self, doc):
        count_groups=int(time.mktime(datetime.now().timetuple()))
        result = self.mongo.db[self.projects_collection].insert({
                                                        'generated_id':str(count_groups)+"-"+slugify(doc['project_name']),
                                                        'slug': slugify(doc['project_name']),
                                                        'project_name': doc['project_name'],
                                                        'year': doc['year'],
                                                        'enabled':"enabled"})
        return result

    def update_project(self, doc):
        result = self.mongo.db[self.projects_collection].update(
            {'generated_id': doc['generated_id']},
            {'generated_id': doc['generated_id'],
             'slug': slugify(doc['project_name']),
             'project_name': doc['project_name'],
             'enabled': doc['enabled_status'],
             'year': doc['year']})
        return result

    def find_selected_project(self,doc):
        result = self.mongo.db[self.projects_collection].find_one({'generated_id':doc['project_gid']})
        return result

    def remove_project(self,doc):
        result = self.mongo.db[self.projects_collection].remove({'generated_id': doc['project_gid']})
        return result

    def get_status(self, doc):
        result = self.mongo.db[self.projects_collection].find_one({'generated_id': doc['generated_id']})
        return result

    def edit_status(self, doc):
        self.mongo.db[self.projects_collection].update({'enabled': {'$in': ['enabled']}},{'$set': {'enabled': 'disabled'}},multi=True)
        result = self.mongo.db[self.projects_collection].update({'generated_id': doc['generated_id']},{'$set':{'enabled':"enabled"}})
        return result

    def get_enabled_project(self):
        result= self.mongo.db[self.projects_collection].find({'enabled':'enabled'})
        return result

    def find_group_project(self,group_slug):
        result = self.mongo.db[self.group_collection].find({'generated_id': group_slug})
        return result

    def find_order_id(self,doc):
        result = self.mongo.db[self.group_collection].find({'order_number': int(doc)})
        return result
    def find_generated_id(self,doc):
        result = self.mongo.db[self.group_collection].find({'generated_id': doc})
        return result


    #def edit_order_group(self,doc):
        result = self.mongo.db[self.projects_collection].find({'enabled': 'enabled'})
        self.mongo.db[self.projects_collection].update(
            {'generated_id': doc['generated_id']},
            {'order_number': doc['order_number']})
        return "fdsf"

    def edit_secound_group(self,generated_id,group_number):
        result = self.mongo.db[self.group_collection].update({'generated_id': generated_id},
                                                                {'$set': {'order_number': int(group_number)}})
        return result

    def edit_first_group(self, generated_id, group_number):
        result = self.mongo.db[self.group_collection].update({'generated_id': generated_id}, {'$set': {'order_number': int(group_number)}})
        return result

    def update_order(self, elements):
        for element in elements:
            result = self.mongo.db[self.group_collection].update({'generated_id': element['generated_id']},{'$set': {'order_number': int(element['order_number'])}})
        return result

    def update_order_questions(self, elements):
        for element in elements:
            result = self.mongo.db[self.questions_collection].update({'question_slug': element['question_slug']},{'$set': {'order_number': int(element['order_number'])}})
        return result

    def find_question_group_ordered(self, doc):
        for element in doc:
            result = self.mongo.db[self.questions_collection].find({'group_slug': element['group_name']})
        return result

    def edit_glasomer_text(self, doc, enabled_year):
        result = self.mongo.db[self.glasomer_text_collection].insert({'glasomer_text':doc['editor1'],'year':enabled_year})
        return result

    def find_glasomer_text(self,enabled_year):
        result = self.mongo.db[self.glasomer_text_collection].find({'year': enabled_year})
        return result

    def delete_glasomer_text(self,enabled_year):
        result = self.mongo.db[self.glasomer_text_collection].remove({'year': enabled_year})
        return result

    def insert_user_session(self, user_id,project_enabled,date):
        result = self.mongo.db[self.visited_users].insert({'user_id':user_id,'year':project_enabled,'date':date})
        return result

    def get_voters_count(self,enabled_year):
        group = {
            '_id': {
                'user_id': '$user_id',
            },
        }
        match = {
            'project_slug': enabled_year,
        }

        pipeline = [
            {'$match': match},
            {'$group': group}
        ]
        result = self.mongo.db[self.answers_users].aggregate(pipeline)
        return result['result']

    def get_visits(self,enabled_year):
        result = self.mongo.db[self.visited_users].find({'year': enabled_year})
        return result
