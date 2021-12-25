from .user_entity import UserEntity, UserCollection
from .user_repository import UserRepository, UserNotFoundException as UserNotFoundRepositoryException
from time import time
import urllib.parse
from random import randint


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def fetch(self, user_id):
        try:
            user_entity = self.user_repository.fetch(user_id)
            return FetchResponse(user_entity)
        except UserNotFoundRepositoryException as e:
            raise UserNotFoundException(e.__str__())

    def confirm_code(self, email, code):
        try:
            user_entity = self.user_repository.confirm_code(
                urllib.parse.unquote(email),
                code
            )
            return FetchResponse(user_entity)
        except UserNotFoundRepositoryException as e:
            raise UserNotFoundException(e.__str__())

    def is_registered(self, email) -> bool:
        return self.user_repository.is_registered(email)

    def fetch_by_email(self, email):
        try:
            user_entity = self.user_repository.fetch_by_email(email)
            return FetchResponse(user_entity)
        except UserNotFoundRepositoryException as e:
            raise UserNotFoundException(e.__str__())

    def create(self, user_entity: UserEntity):
        try:
            user_entity.user['code'] = randint(000000, 999999)
            user_entity.user['verifiedEmail'] = False
            user_entity = self.user_repository.create(user_entity)
            return CreateUserResponse(user_entity)
        except UserNotFoundRepositoryException as e:
            raise UserNotFoundException(e.__str__())


class CreateUserResponse:

    def __init__(self, user_entity: UserEntity):
        self.user_entity = user_entity

    def to_dict(self):
        return self.user_entity.to_dict()


class FetchResponse:

    def __init__(self, user_entity: UserEntity):
        self.user_entity = user_entity

    def to_dict(self):
        return self.user_entity.to_dict()


class UserNotFoundException(Exception):
    def __init__(self, message):
        super(UserNotFoundException, self).__init__(message)
