

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""


import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configurando la firma de JWT
app.config['JWT_SECRET_KEY'] = os.environ.get("FLASK_APP_KEY")

MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)
JWTManager(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
"""
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response

@app.route('/signup', methods=['POST'])
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
        return jsonify({"error": f"{error}"}), 500

@app.route('/login', methods=['POST'])
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

@app.route('/private', methods=['GET'])
@jwt_required()
def private():

    try:
        return jsonify({"message": "Authenticated successfully!"})
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)"""
