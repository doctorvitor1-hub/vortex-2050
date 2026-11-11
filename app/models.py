from datetime import datetime
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_type = db.Column(db.String(20), default='digital')  # 'digital' ou 'physical' no futuro
    file_name = db.Column(db.String(150), nullable=True)        # Arquivo dentro de digital_assets/
    cover_badge = db.Column(db.String(50), default='TRENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_session_id = db.Column(db.String(255), unique=True, nullable=False)
    customer_email = db.Column(db.String(150), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='pending')        # 'pending' ou 'paid'
    access_token = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product')
