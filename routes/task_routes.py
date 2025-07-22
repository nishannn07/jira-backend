# routes/task_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.task_controller import (
    create_task, update_task, get_task_with_details, get_tasks_by_user,
    add_comment, log_time, get_project_tasks_by_status, get_comment_by_task_id, get_tasks_by_project_id
)


tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('/new', methods=['POST'])
@jwt_required()
def new_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    task = create_task(data, current_user)
    return jsonify({"message": "Task created successfully", "task": task.to_dict()}), 201


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def view_task(task_id):
    task = get_task_with_details(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200


@tasks_bp.route('/<int:task_id>/edit', methods=['PUT'])
@jwt_required()
def edit_task(task_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    task = update_task(task_id, data, current_user_id)
    return jsonify({"message": "Task updated successfully", "task": task.to_dict()}), 200


@tasks_bp.route('/<int:task_id>/comment', methods=['POST'])
@jwt_required()
def add_task_comment(task_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    comment = add_comment(task_id, data.get('content'), current_user)
    return jsonify({"message": "Comment added successfully", "comment": comment.to_dict()}), 201

@tasks_bp.route('/<int:task_id>/comments')
@jwt_required()
def get_task_comment(task_id):
    comments = get_comment_by_task_id(task_id)
    return jsonify([comment.to_dict() for comment in comments]), 200

@tasks_bp.route('/<int:task_id>/time', methods=['POST'])
@jwt_required()
def log_task_time(task_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    time_log = log_time(task_id, data.get('hours_spent'), data.get('description'), data.get('work_date'), current_user)
    return jsonify({"message": "Time logged successfully", "time_log": time_log.to_dict()}), 201


@tasks_bp.route('/my-tasks', methods=['GET'])
@jwt_required()
def my_tasks():
    current_user = get_jwt_identity()
    tasks = get_tasks_by_user(current_user)
    print(tasks)
    return jsonify([task.to_dict() for task in tasks]), 200


@tasks_bp.route('/project/<int:project_id>/board', methods=['GET'])
@jwt_required()
def kanban_board(project_id):
    board = get_project_tasks_by_status(project_id)
    return jsonify({key: [t.to_dict() for t in value] for key, value in board.items()}), 200

@tasks_bp.route('/project-tasks/<int:project_id>', methods=['GET'])
@jwt_required()
def pro_tasks(project_id):
    tasks = get_tasks_by_project_id(project_id)
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('/story/<int:story_id>', methods=['GET'])
@jwt_required()
def get_story_tasks(story_id):
    from models.task import Task
    tasks = Task.query.filter_by(story_id=story_id, is_deleted=False).all()
    return jsonify([task.to_dict() for task in tasks]), 200
