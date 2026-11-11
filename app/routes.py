import os
import uuid
import stripe
from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort, current_app
from app import db
from app.models import Product, Order, OrderItem

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    category = request.args.get('category', 'Todas')
    search = request.args.get('q', '').strip()

    query = Product.query
    if category and category != 'Todas':
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%') | Product.description.ilike(f'%{search}%'))

    products = query.order_by(Product.id.asc()).all()
    categories = ['Todas', 'IA & Automação', 'Renda Digital', 'Biohacking & Saúde', 'Finanças Modernas', 'Produtividade Extrema', 'Estética & Lifestyle']
    
    return render_template('index.html', products=products, categories=categories, active_category=category, search=search)

@main_bp.route('/produto/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    related = Product.query.filter(Product.category == product.category, Product.id != product.id).limit(3).all()
    return render_template('product.html', product=product, related=related)

@main_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    domain_url = os.getenv('DOMAIN_URL', 'http://127.0.0.1:5000').rstrip('/')

    data = request.get_json()
    item_ids = data.get('items', [])

    if not item_ids:
        return jsonify({'error': 'Carrinho vazio.'}), 400

    products = Product.query.filter(Product.id.in_(item_ids)).all()
    if not products:
        return jsonify({'error': 'Produtos não encontrados.'}), 404

    line_items = []
    total_amount = 0.0

    for p in products:
        total_amount += p.price
        line_items.append({
            'price_data': {
                'currency': 'brl',
                'product_data': {
                    'name': p.title,
                    'description': f"Edição Digital VORTEX 2050 • {p.category}",
                },
                'unit_amount': int(round(p.price * 100)),
            },
            'quantity': 1,
        })

    access_token = uuid.uuid4().hex

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f"{domain_url}/pedido/{access_token}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/",
            metadata={
                'access_token': access_token
            }
        )

        order = Order(
            stripe_session_id=checkout_session.id,
            total_amount=total_amount,
            status='pending',
            access_token=access_token
        )
        db.session.add(order)
        db.session.flush()

        for p in products:
            db.session.add(OrderItem(order_id=order.id, product_id=p.id))

        db.session.commit()
        return jsonify({'url': checkout_session.url})

    except Exception as e:
        return jsonify({'error': f'Erro Stripe: {str(e)}'}), 500

@main_bp.route('/pedido/<access_token>')
def order_success(access_token):
    order = Order.query.filter_by(access_token=access_token).first_or_404()
    session_id = request.args.get('session_id')

    # Verificação direta na API da Stripe (garante liberação imediata mesmo antes do webhook chegar)
    if order.status != 'paid' and session_id:
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                order.status = 'paid'
                order.customer_email = session.customer_details.email if session.customer_details else None
                db.session.commit()
        except Exception:
            pass

    return render_template('success.html', order=order)

@main_bp.route('/download/<access_token>/<int:product_id>')
def download_ebook(access_token, product_id):
    order = Order.query.filter_by(access_token=access_token, status='paid').first_or_404()
    item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first_or_404()

    assets_dir = os.path.join(os.path.dirname(current_app.root_path), 'digital_assets')
    return send_from_directory(assets_dir, item.product.file_name, as_attachment=True)
