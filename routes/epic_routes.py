from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.epic_controller import (
    create_epic, get_epics_by_project, get_epic_by_id, 
    update_epic, delete_epic
)

epic_bp = Blueprint('epics', __name__, url_prefix='/api/epics')

@epic_bp.route('/new', methods=['POST'])
@jwt_required()
def new_epic():
    user_id = get_jwt_identity()
    data = request.get_json()
    epic = create_epic(data, user_id)
    return jsonify({"message": "Epic created successfully", "epic": epic.to_dict()}), 201

@epic_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_epics(project_id):
    epics = get_epics_by_project(project_id)
    return jsonify([epic.to_dict() for epic in epics]), 200

@epic_bp.route('/<int:epic_id>', methods=['GET'])
@jwt_required()
def get_epic(epic_id):
    epic = get_epic_by_id(epic_id)
    if not epic:
        return jsonify({"error": "Epic not found"}), 404
    return jsonify(epic.to_dict()), 200

@epic_bp.route('/<int:epic_id>/edit', methods=['PUT'])
@jwt_required()
def edit_epic(epic_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    epic = update_epic(epic_id, data, user_id)
    return jsonify({"message": "Epic updated successfully", "epic": epic.to_dict()}), 200

@epic_bp.route('/<int:epic_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_epic_route(epic_id):
    delete_epic(epic_id)
    return jsonify({"message": "Epic deleted successfully"}), 200
