from pymongo.cursor import Cursor


class UserEntity:

    def __init__(self, user):
        self.user = user

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data)

    def to_dict(self):
        return self.user

    @classmethod
    def from_mongodb_document(cls, document: dict):
        document['userId'] = str(document['_id'])
        del (document['_id'])
        del (document['password'])
        return cls(document)

    def to_mongodb_document(self):
        return self.user


class UserCollection:

    def __init__(self, users):
        self.users = users

    @classmethod
    def from_mongodb_cursor(cls, cursor: Cursor):
        users = []
        for user in cursor:
            users.append(UserEntity.from_mongodb_document(user))
        return cls(users)

    def to_dict(self):
        users = []
        for user in self.users:
            users.append(user.to_dict())
        return users
