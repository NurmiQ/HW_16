import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import data


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('Order', foreign_keys=[order_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


db.create_all()

for user_data in data.users:
    new_user = User(
        id=user_data['id'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        age=user_data['age'],
        email=user_data['email'],
        role=user_data['role'],
        phone=user_data['phone'],
    )
    db.session.add(new_user)
    db.session.commit()

for order_data in data.orders:
    new_order = Order(
        id=order_data['id'],
        name=order_data['name'],
        description=order_data['description'],
        start_date=order_data['start_date'],
        end_date=order_data['end_date'],
        address=order_data['address'],
        price=order_data['price'],
        customer_id=order_data['customer_id'],
        executor_id=order_data['executor_id'],
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in data.offers:
    new_offer = Offer(
        id=offer_data['id'],
        order_id=offer_data['order_id'],
        executor_id=offer_data['executor_id'],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users", methods=["POST", "GET"])
def all_users():
    if request.method == 'GET':
        users_response = []
        users = User.query.all()
        for user in users:
            users_response.append(
                {"id": user.id,
                 "first_name": user.first_name,
                 "last_name": user.last_name,
                 "age": user.age,
                 "email": user.email,
                 "role": user.role,
                 "phone": user.phone,
                 }
            )
        return jsonify(users_response)
    elif request.method == 'POST':
        data = request.json
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone'),
            )
        db.session.commit()
        return jsonify({
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "age": new_user.age,
            "email": new_user.email,
            "role": new_user.role,
            "phone": new_user.phone,
            })


@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def get_user(uid: int):
    if request.method == 'GET':
        user = User.query.get(uid)
        if user is None:
            return "user not found"
        return jsonify({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone,
            })
    elif request.method == "DELETE":
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return jsonify(" ")
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(uid)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']

        db.session.add(user)
        db.session.commit()
        return jsonify(" ")


@app.route("/orders", methods=["POST", "GET"])
def all_orders():
    if request.method == 'GET':
        orders_response = []
        orders = Order.query.all()
        for order in orders:
            orders_response.append(
                {"id": order.id,
                 "name": order.name,
                 "description": order.description,
                 "start_date": order.start_date,
                 "end_date": order.end_date,
                 "address": order.address,
                 "price": order.price,
                 }
            )
        return jsonify(orders_response)
    elif request.method == 'POST':
        data = request.json
        new_order = Order(
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            address=data.get('address'),
            price=data.get('price'),
            )
        db.session.commit()
        return jsonify({
            "id": new_order.id,
            "name": new_order.name,
            "description": new_order.description,
            "start_date": new_order.start_date,
            "end_date": new_order.end_date,
            "address": new_order.address,
            "price": new_order.price,
            })


@app.route("/orders/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def get_orders(oid: int):
    if request.method == 'GET':
        order = Order.query.get(oid)
        if order is None:
            return "order not found"
        return jsonify({
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            })
    elif request.method == "DELETE":
        order = Order.query.get(oid)
        db.session.delete(order)
        db.session.commit()
        return jsonify(" ")
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        order = Order.query.get(oid)
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = order_data['start_date']
        order.end_date = order_data['end_date']
        order.address = order_data['address']
        order.price = order_data['price']

        db.session.add(order)
        db.session.commit()
        return jsonify(" ")

@app.route("/offers", methods=["POST", "GET"])
def all_offers():
    if request.method == 'GET':
        offers_response = []
        offers = Offer.query.all()
        for offer in offers:
            offers_response.append(
                {"id": offer.id,
                 "order_id": offer.order_id,
                 "executor_id": offer.executor_id,
                 }
            )
        return jsonify(offers_response)
    elif request.method == 'POST':
        data = request.json
        new_offer = Offer(
            order_id=data.get('order_id'),
            executor_id=data.get('executor_id'),
            )
        db.session.commit()
        return jsonify({
            "id": new_offer.id,
            "order_id": new_offer.order_id,
            "executor_id": new_offer.executor_id,
            })


@app.route("/offers/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def get_offers(oid: int):
    if request.method == 'GET':
        offer = Offer.query.get(oid)
        if offer is None:
            return "offer not found"
        return jsonify({
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id,
            })
    elif request.method == "DELETE":
        offer = Offer.query.get(oid)
        db.session.delete(offer)
        db.session.commit()
        return jsonify(" ")
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = User.query.get(oid)
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        return jsonify(" ")


if __name__ == "__main__":
    app.run()
