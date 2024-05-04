from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://frambu_user:TJJPvqjdRaT20148FLKkKxW03EkeseC4@dpg-cor77li0si5c739d5k60-a.oregon-postgres.render.com/frambu'
db = SQLAlchemy(app)

class Order(db.Model):
    STATE_CHOICES = [
        ('payment_pending', 'Payment Pending'),
        ('paid', 'Paid'),
        ('in_production', 'In Production'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False, default=uuid.uuid4)
    product_type = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(40), nullable=False, default='payment_pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    quantity = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    profits = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Order('{self.name}', '{self.state}')"
    
@app.route('/create', methods=['GET'])
def create_table():
    db.create_all()
    return 'Tabla creada'

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify({'orders': [{'name': order.name, 'state': order.state} for order in orders]})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'name': order.name, 'state': order.state})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(product_type=data['product_type'], state=data['state'], quantity=data['quantity'], paid=data['paid'], profits=data['profits'])
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.state = data['state']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

@app.route('/')
def index():
    return 'API Frambuu'

if __name__ == '__main__':
    app.run(debug=True)
