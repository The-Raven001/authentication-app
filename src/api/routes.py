"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def user_signup():
    try:
        body = request.json
        email = body.get('email', None)
        password = body.get('password', None)
        
        if email is None or password is None:
            return jsonify({"error":"Password and email are required"}), 400

        email_is_taken = User.query.filter_by(email=email).first()
        if email_is_taken:
            return jsonify({"error": "email is in usage already."}), 400

        password_hash = generate_password_hash(password)

        user = User(email=email, password=password_hash)

        db.session.add(user)
        db.session.commit()
        
        return jsonify({"msg": "User created"}), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500\


@api.route('/login', methods=['POST'])
def login():
    try:
        body = request.json
        email = body.get('email', None)
        password = body.get('password', None) 

        if email is None or password is None:
            return jsonify({'error': 'password and email are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"error": "user not found"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"error": "password or user not matching"}), 400

        auth_token = create_access_token({"id": user.id, "email": user.email})
        return jsonify({"token": auth_token}), 200

    except Exception as error:
        return jsoninfy({"error": f"{error}"})

@api.route('/private', methods=['GET'])
@jwt_required()
def private():

    try:
        return jsonify({"message": "Authenticated successfully!"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    api.run(host='0.0.0.0', port=PORT, debug=True)