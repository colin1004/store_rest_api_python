import sqlite3
from db import db
# resource is external representation of Entity
# model is internal representation of Entity
# extend db.Model for orm
class UserModel(db.Model):
    # orm table set
    __tablename__ = 'users'
    # orm property set
    id = db.Column(db.Integer, primary_key=True) # automatic assign new id
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SELECT * FROM users WHERE username=username LIMIT 1

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
