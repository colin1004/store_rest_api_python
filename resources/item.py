from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# resource is external representation of Entity
# model is internal representation of Entity
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = "Every item needs a store id!"
    )
    # API
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    # API
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400 ## request error


        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # simple way
        # item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # interal server error

        return item.json(), 201

    # API
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # API
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    # API
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}
        # return {'items':list(map(lambda x:x.json(),ItemModel.query.all()))}
