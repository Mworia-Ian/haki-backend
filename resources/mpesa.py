from flask import request, jsonify
from flask_restful import Resource
import base64
import requests
from datetime import datetime, timedelta
from models import db, Payment
from flask_jwt_extended import jwt_required

# Global variable to store the token and its expiration
token_info = {
    'token': None,
    'expires_at': None
}

def create_token():
    secret = '8JltK44JOAaiGrGxk3cNADBF6AFpNEebmJvF9Wf7jvrWS7ZsDM9QBgza3mfFfTON'
    consumer = '4YWMPAsbwOM3iSvbAJHEn0udpIeLkqKtLdKSYFNkuP7g4NeA'
    auth = base64.b64encode(f"{consumer}:{secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth}'
    }

    response = requests.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers=headers)

    if response.status_code == 200:
        data = response.json()
        token_info['token'] = data['access_token']
        token_info['expires_at'] = datetime.utcnow() + timedelta(minutes=59)  # Token valid for 60 minutes
        return True, None
    else:
        return False, response.text

def get_token():
    if token_info['token'] is None or datetime.utcnow() >= token_info['expires_at']:
        success, error = create_token()
        if not success:
            return None
    return token_info['token']

class StkPush(Resource):
    @jwt_required()
    def post(self):
        token = get_token()
        if token is None:
            return jsonify({'error': 'Failed to get token'}), 500

        request_data = request.get_json()
        phone = request_data.get('phone')
        amount = request_data.get('amount')
        user_id = request_data.get('user_id')

        if not phone or not amount or not user_id:
            return jsonify({'error': 'Phone number, amount, and user_id are required'}), 400

        phone = phone.lstrip('0')  # Remove the leading 0
        short_code = 174379
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{short_code}{passkey}{timestamp}".encode()).decode()

        data = {
            'BusinessShortCode': short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': f"254{phone}",
            'PartyB': short_code,
            'PhoneNumber': f"254{phone}",
            'CallBackURL': 'https://mydomain.com/path',
            'AccountReference': 'Mpesa Test',
            'TransactionDesc': 'Testing stk push'
        }

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            transaction_id = response_data.get('CheckoutRequestID')
            
            # Save payment to database
            try:
                new_payment = Payment(
                    user_id=user_id,
                    amount=amount,
                    transaction_id=transaction_id,
                    status='pending'
                )
                db.session.add(new_payment)
                db.session.commit()
                
                return jsonify({'message': 'STK Push initiated successfully', 'transaction_id': transaction_id}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Failed to save payment to database: {str(e)}'}), 500
        else:
            return jsonify({'error': response.text}), response.status_code
