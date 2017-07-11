from drongo.utils import dict2

from bson.objectid import ObjectId

import pickle


DEFAULT = pickle.dumps(dict2())


class Mongo(object):
    def __init__(self, **config):
        self.collection = config.get('collection')

    def load(self, session_id):
        try:
            sess = self.collection.find_one(dict(_id=ObjectId(session_id)))
            session = pickle.loads(sess['value'])
        except Exception as _:
            sess = {'value': DEFAULT}
            session_id = str(self.collection.insert_one(sess).inserted_id)
            session = pickle.loads(sess['value'])
            session._sessid = session_id

        return session

    def save(self, session):
        session_id = session._sessid
        self.collection.update_one(dict(_id=ObjectId(session_id), {
            '$set': session
        }))
