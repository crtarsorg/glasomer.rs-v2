from slugify import slugify
from bson import json_util
class MongoUtils(object):


    def __init__(self, mongo):
        self.mongo = mongo
        self.group_collection = "group_collection"
        self.questions_collection = "questions_collection"
        self.candidates_collection = "candidates_collection"
        self.answers_candidates = "answers_candidates"
        self.answers_users = "answers_users"
    def insert_question(self, doc):
        count_groups=self.mongo.db[self.group_collection].count()
        result = self.mongo.db[self.group_collection].insert({'generated_id':str(count_groups)+"-"+slugify(doc['group_name']),'slug': slugify(doc['group_name']), 'group_name': doc['group_name'],'order_number':doc['order_number']})
        return result

    def find_group(self, slug):
        result = self.mongo.db[self.group_collection].find_one({'slug': slug})
        return result

    def find_all(self):
        result = self.mongo.db[self.group_collection].find().sort('order_number')
        return result

    def find_all_questions(self):
        result = self.mongo.db[self.questions_collection].find().sort('order_number')
        return result

    def count_groups(self):
        result = self.mongo.db[self.group_collection].count()
        return result
    def find_selected_group(self,doc):
        result = self.mongo.db[self.group_collection].find_one({'generated_id':doc['group_name']})
        return result

    def update_selected_group(self,doc):
        print doc['hidden_group']
        result = self.mongo.db[self.group_collection].update({'generated_id': doc['hidden_group']},{'slug': slugify(doc['group_name']),'group_name': doc['group_name'],'order_number':doc['order_number'],'generated_id': doc['hidden_group']}, upsert=False)
        return result

    def remove_group(self,doc):
        result = self.mongo.db[self.group_collection].remove({'generated_id': slugify(doc['group_name'])})
        return result

    def find_questions(self, doc):
        result = self.mongo.db[self.questions_collection].find({'group_slug': doc['group_name']})
        return result

    def insert_question_group(self, doc):
        question_name=doc['question_name']
        self.mongo.db[self.questions_collection].insert({'group_slug': doc['group_name'],"question_name" :question_name,'question_slug':slugify(question_name),'order_number':doc['order_number']})
        result = self.mongo.db[self.group_collection].find()
        return result


    def find_selected_question(self, doc):
        result=self.mongo.db[self.questions_collection].find({'question_slug': doc['question_slug']})
        return result

    def update_selected_question(self, doc):
        result = self.mongo.db[self.questions_collection].update({'question_slug':doc['hidden_question']},{'question_slug': slugify(doc['question_name']),'question_name': doc['question_name'],'order_number': doc['order_number'],'group_slug':doc['group_name']}, upsert=False)
        return result

    def find_question_group(self, doc):
        result = self.mongo.db[self.questions_collection].find({'group_slug': doc['group_name']})
        return result

    def delete_question(self,doc):
        result = self.mongo.db[self.questions_collection].remove({'question_slug': slugify(doc['question_slug'])})
        return result


    def insert_candidate(self, doc, filename):
        count_groups=self.mongo.db[self.candidates_collection].count()
        result = self.mongo.db[self.candidates_collection].insert({
                                                        'generated_id':str(count_groups)+"-"+slugify(doc['candidate_name']),
                                                        'slug': slugify(doc['candidate_name']),
                                                        'candidate_name': doc['candidate_name'],
                                                        'candidate_biography': doc['candidate_biography'],
                                                        'image': filename},upsert=False)
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

        result = self.mongo.db[self.answers_candidates].remove({'candidate_slug': slugify(doc['candidate_slug'])})
        result = self.mongo.db[self.answers_candidates].insert(doc)

    def get_candidate_asnwers(self,candidate_url):
        result = self.mongo.db[self.answers_candidates].find({'candidate_slug':candidate_url})
        return result

    def get_nr_questions(self):
        result = self.mongo.db[self.questions_collection].count()
        return result

    def insert_users_answers(self, doc):
        print doc['user_id']
        self.mongo.db[self.answers_users].remove({'user_id': doc['user_id']})
        self.mongo.db[self.answers_users].insert(doc)
        result_candidates=self.mongo.db[self.answers_candidates].find()
        result_user=self.mongo.db[self.answers_users].find({'user_id':doc['user_id']})
        candidates=self.mongo.db[self.candidates_collection].find()
        all_question=self.mongo.db[self.questions_collection].find()
        return {'user_results':result_user, 'candidate_results':result_candidates,'candidates':candidates,'all_question':all_question}

