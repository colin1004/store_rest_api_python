from db import db

class StoreModel(db.Model):
    # orm table set
    __tablename__ = 'stores'
    # orm property set
    id = db.Column(db.Integer, primary_key=True) # automatic assign new id
    name = db.Column(db.String(80))

    # add relationship with ItemModel - many to one
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
