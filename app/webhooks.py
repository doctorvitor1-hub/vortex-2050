import os
import stripe
from flask import Blueprint, request, jsonify
from app import db
from app.models import Order

webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    try:
        if webhook_secret and not webhook_secret.startswith('whsec_sua_chave'):
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = request.get_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.get('payment_status') == 'paid':
            order = Order.query.filter_by(stripe_session_id=session['id']).first()
            if order:
                order.status = 'paid'
                customer_details = session.get('customer_details') or {}
                order.customer_email = customer_details.get('email')
                db.session.commit()

    return jsonify({'status': 'success'}), 200
