from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.activity_controller import get_activities_by_user

activity_bp = Blueprint('activity_bp', __name__, url_prefix='/api/activities')

@activity_bp.route('/user', methods=['GET'])
@jwt_required()
def user_activity_logs():
    user_id = get_jwt_identity()
    activities = get_activities_by_user(user_id)
    return jsonify([activity.to_dict() for activity in activities]), 200
