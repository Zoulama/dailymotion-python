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
