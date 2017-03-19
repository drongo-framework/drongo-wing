from datetime import datetime
from passlib.hash import pbkdf2_sha256

import uuid


class AuthBackend(object):
    pass


class AuthMongoBackend(AuthBackend):
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

    def create_user(self, username, password, active=False):
        user = self.collection.find_one({
            'username': username,
        })
        if user is not None:
            raise Exception('User already exists!')

        user = {
            'username': username,
            'password': pbkdf2_sha256.hash(password),
            'active': False,
            'activation_code': uuid.uuid4().hex,
            'registered_on': datetime.utcnow()
        }
        self.collection.insert_one(user)

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
