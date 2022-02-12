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











#
#
# @app.route("/guides/<int:gid>/delete")
# def delete_guide(gid):
#     guide = Guide.query.get(gid)
#     db.session.delete(guide)
#     db.session.commit()
#     return jsonify(" ")
#
#
# @app.route("/guides", methods=['POST'])
# def create_guide():
#     data = request.json
#     guide = Guide(
#         surname=data.get('surname'),
#         full_name=data.get('full_name'),
#         tours_count=data.get('tours_count'),
#         bio=data.get('bio'),
#         is_pro=data.get('is_pro'),
#         company=data.get('company')
#     )
#     db.session.commit()
#     return jsonify({
#         "id": guide.id,
#         "surname": guide.surname,
#         "full_name": guide.full_name,
#         "tours_count": guide.tours_count,
#         "bio": guide.bio,
#         "is_pro": guide.is_pro,
#         "company": guide.company
#     })


if __name__ == "__main__":
    app.run()
