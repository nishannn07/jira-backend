from flask import Flask, redirect, url_for, request, jsonify
from flask_migrate import Migrate
from flask_mailman import Mail
from models import db
import models.user, models.project, models.task, models.role, models.comment, models.login, models.dashboard, models.notification, models.team
from routes import register_blueprints
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from seed.role_seeder import seed_roles
from seed.create_super_admin import create_super_admin_command
from flask_jwt_extended.exceptions import JWTExtendedException
from flask import jsonify
from jwt.exceptions import DecodeError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, origins='*')
app.cli.add_command(seed_roles)
app.cli.add_command(create_super_admin_command)
mail = Mail(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(err):
    return jsonify({"msg": "Missing or invalid token", "error": err}), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(err):
    return jsonify({"msg": "Invalid token", "error": err}), 422

@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return jsonify({"msg": "Token expired"}), 401

@jwt.needs_fresh_token_loader
def custom_needs_fresh_token_response(jwt_header, jwt_payload):
    return jsonify({"msg": "Fresh token required"}), 401

register_blueprints(app)

@app.route('/')
def home():
    return redirect(url_for('main_bp.dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
