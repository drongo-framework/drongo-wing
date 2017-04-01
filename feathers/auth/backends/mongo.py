from datetime import datetime
from passlib.hash import pbkdf2_sha256

import uuid


class MongoBackend(object):
    def __init__(self, connection):
        self.connection = connection
        self.collection = connection.auth_users

    def verify_login(self, username, password):
        user = self.collection.find_one({
            'username': username,
        })
        if user is None:
            raise Exception('Invalid username/password.')

        if not pbkdf2_sha256.verify(password, user['password']):
            raise Exception('Invalid username/password.')

        if not user['active']:
            raise Exception('User account is not active!')

    def user_exists(self, username):
        user = self.collection.find_one({
            'username': username,
        })
        return user is not None

    def create_user(self, username, password, active=False):
        user = self.collection.find_one({
            'username': username,
        })
        if user is not None:
            raise Exception('User already exists!')

        user = {
            'username': username,
            'password': pbkdf2_sha256.hash(password),
            'active': active,
            'activation_code': uuid.uuid4().hex,
            'registered_on': datetime.utcnow()
        }
        self.collection.insert_one(user)

    def update_user(self, username, fields={}):
        user = self.collection.find_one({
            'username': username,
        })
        self.collection.update_one(
            {'_id': user['_id']},
            {
                '$set': fields
            }
        )

    def activate_user(self, username, code):
        user = self.collection.find_one({
            'username': username,
        })

        if user is None:
            raise Exception('Activation failure!')

        if code != user['activation_code']:
            raise Exception('Activation failure!')

        self.collection.update_one(
            {'_id': user['_id']},
            {
                '$set': {
                    'active': True
                }
            }
        )
