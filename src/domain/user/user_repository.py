from flask import Flask, jsonify
from pymongo.collection import Collection
from bson import ObjectId
import urllib.parse

from flask_bcrypt import Bcrypt
from src.domain.user.user_entity import UserEntity, UserCollection

app = Flask(__name__)
bcrypt = Bcrypt()


class UserRepository:

    def __init__(self, mongodb_user_collection: Collection):
        self.mongodb_user_collection = mongodb_user_collection

    def create(self, user_entity: UserEntity) -> UserEntity:
        app.logger.info(user_entity.user['password'])

        user_entity.user['password'] = bcrypt.generate_password_hash(user_entity.user['password'])
        insert_one_result = self.mongodb_user_collection.insert_one(user_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch(self, user_id) -> UserEntity:
        document = self.mongodb_user_collection.find_one({'_id': ObjectId(user_id)})
        if document is None:
            raise UserNotFoundException('user %s not found' % user_id)
        return UserEntity.from_mongodb_document(document)

    def confirm_code(self, email, code) -> UserEntity:
        document = self.mongodb_user_collection.find_one({
            'email': urllib.parse.unquote(email)
        })

        if document:
            user_entity = UserEntity.from_mongodb_document(document)
            user_id = user_entity.user['userId']
            if user_entity.user['code'] == 0 and user_entity.user['verifiedEmail'] is True:
                raise UserNotFoundException('email %s already confirmed' % email)
            document_code = self.mongodb_user_collection.find_one({
                'code': int(code)
            })
            if document_code is None:
                raise UserNotFoundException('code confirmation %s not valid' % code)
            user_entity.user['code'] = 0
            user_entity.user['verifiedEmail'] = True
            update_one_result = self.mongodb_user_collection.update_one({'_id': ObjectId(user_id)},
                                                                        {'$set': user_entity.to_mongodb_document()})
            return self.fetch(user_id)
        raise UserNotFoundException('user %s not found' % email)

    def fetch_by_email(self, email) -> UserEntity:
        document = self.mongodb_user_collection.find_one({'email': email})
        if document:
            raise UserNotFoundException('user %s not found' % email)
        return UserEntity.from_mongodb_document(document)

    def is_registered(self, email) -> bool:
        document = self.mongodb_user_collection.find_one({'email': email})
        if document:
            return True
        else:
            return False


class UserNotFoundException(Exception):
    def __init__(self, message):
        super(UserNotFoundException, self).__init__(message)
