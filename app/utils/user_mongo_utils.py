from bson.objectid import ObjectId


class UserMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.users_collection = 'user'
