#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods = ['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response([restaurant.to_dict() for restaurant in restaurants], 200)

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)
    if request.method == 'GET':
        return make_response(restaurant.to_dict(), 200)
    elif request.method == 'DELETE':
        restaurant_pizzas = RestaurantPizza.query.all()
        for restaurant_pizza in restaurant_pizzas:
            if restaurant_pizza.restaurant.id == id:
                db.session.delete(restaurant_pizza)
                db.session.commit()
        db.session.delete(restaurant)
        db.session.commit()

        return make_response({"restaurant successfully deleted"}, 200)

@app.route('/pizzas', methods = ['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response([pizza.to_dict() for pizza in pizzas], 200)

@app.route('/restaurant_pizzas', methods = ['POST'])
def new_restaurant_pizza():
    try:
        new_rp = RestaurantPizza(
            price = request.get_json()['price'],
            pizza_id = request.get_json()['pizza_id'],
            restaurant_id = request.get_json()['restaurant_id']
        )
        db.session.add(new_rp)
        db.session.commit()

        pizza = Activity.query.filter_by(id=new_rp.pizza.id).first()
        return make_response(pizza.to_dict(), 200)
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
