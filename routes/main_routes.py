from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.project_controller import get_user_projects
from controllers.task_controller import get_tasks_by_user, search_tasks
from controllers.user_controller import *
from models.activity_log import ActivityLog
from models.notification import Notification

main_bp = Blueprint('main_bp', __name__, url_prefix='/api')

@main_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    id = int(get_jwt_identity())
    user = get_user_by_id(id)

    projects = [p.to_dict() for p in get_user_projects(user.id)]
    tasks = [t.to_dict() for t in get_tasks_by_user(user.id)]
    activities = [a.to_dict() for a in ActivityLog.query.filter_by(user_id=user.id).order_by(ActivityLog.created_at.desc()).limit(5)]

    return jsonify({"projects": projects, "tasks": tasks, "activities": activities})

   

@main_bp.route('/search')
@jwt_required()
def search():
    id = get_jwt_identity()
    user = get_user_by_id(id)
    query = request.args.get('q', '')
    tasks = [t.to_dict() for t in search_tasks(query, user.id)] if query else []
    return jsonify({"tasks": tasks})

@main_bp.route('/for-you')
@jwt_required()
def for_you():
    id = get_jwt_identity()
    user = get_user_by_id(id)
    tasks = [t.to_dict() for t in get_tasks_by_user(user.id)]
    project_ids = [p.id for p in get_user_projects(user.id)]
    activities = [a.to_dict() for a in ActivityLog.query.filter(ActivityLog.project_id.in_(project_ids)).order_by(ActivityLog.created_at.desc()).limit(20)]
    return jsonify({"tasks": tasks, "activities": activities})

@main_bp.route('/notifications')
@jwt_required()
def get_notifications():
    id = get_jwt_identity()
    user = get_user_by_id(id)
    notifications = [n.to_dict() for n in Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc())]
    return jsonify({"notifications": notifications})
