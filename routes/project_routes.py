from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.project_controller import (
    create_project, update_project, get_user_projects, get_project_with_stats,
    delete_project, get_all_projects, update_project_status, get_all_projects_with_teams
)
from controllers.task_controller import get_project_tasks_by_status
from rba_decoder import role_required

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')
from rba_decoder import *

@projects_bp.route('/', methods=['GET'])
@jwt_required()
def list_projects():
    user_id = int(get_jwt_identity())
    projects = get_user_projects(user_id)
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route('/new', methods=['POST'])
@role_required("manager", "admin", "super_admin")
def new_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    project = create_project(data, user_id)
    return jsonify(project.to_dict()), 201


@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def view_project(project_id):
    project, stats = get_project_with_stats(project_id)
    return jsonify({
        'project': project.to_dict(),
        'stats': stats
    }), 200

@projects_bp.route('/<int:project_id>/edit_status', methods=['PUT'])
@role_required('manager', 'super_admin')
def edit_project_status(project_id):
    data = request.get_json()
    print(data)
    current_user_id = get_jwt_identity()
    try:
        update_project_status(current_user_id, project_id, data)
        return jsonify({"message": "Status updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@projects_bp.route('/<int:project_id>/board', methods=['GET'])
@jwt_required()
def kanban_board(project_id):
    print(project_id)
    project, stats = get_project_with_stats(project_id)
    task_board = get_project_tasks_by_status(project_id)
    return jsonify({
        'project': project.to_dict(),
        'stats': stats,
        'task_board': {
            k: [t.to_dict() for t in v] for k, v in task_board.items()
        }
    }), 200


@projects_bp.route('/<int:project_id>/edit', methods=['PUT'])
@jwt_required()
def edit_project(project_id):
    data = request.get_json()
    project = update_project(project_id, data)
    return jsonify(project.to_dict()), 200


@projects_bp.route('/<int:project_id>/delete', methods=['DELETE'])
@jwt_required()
@role_required('manager', 'super_admin')
def delete_project_route(project_id):
    delete_project(project_id)
    return jsonify({'message': 'Project deleted successfully.'}), 200

@projects_bp.route('/super-admin/all-projects', methods=['GET'])
@role_required('super_admin')
def get_all_projects_for_super_admin():
    """
    Provides a list of all projects with their associated teams.
    Accessible only by super admins.
    """
    projects = get_all_projects_with_teams()
    return jsonify([p.to_dict() for p in projects]), 200