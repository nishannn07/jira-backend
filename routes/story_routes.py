from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.story_controller import (
    create_story, get_stories_by_epic, get_stories_by_project,
    get_story_by_id, update_story, delete_story
)

story_bp = Blueprint('stories', __name__, url_prefix='/api/stories')

@story_bp.route('/new', methods=['POST'])
@jwt_required()
def new_story():
    user_id = get_jwt_identity()
    data = request.get_json()
    story = create_story(data, user_id)
    return jsonify({"message": "Story created successfully", "story": story.to_dict()}), 201

@story_bp.route('/epic/<int:epic_id>', methods=['GET'])
@jwt_required()
def get_epic_stories(epic_id):
    stories = get_stories_by_epic(epic_id)
    return jsonify([story.to_dict() for story in stories]), 200

@story_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_stories(project_id):
    stories = get_stories_by_project(project_id)
    return jsonify([story.to_dict() for story in stories]), 200

@story_bp.route('/<int:story_id>', methods=['GET'])
@jwt_required()
def get_story(story_id):
    story = get_story_by_id(story_id)
    if not story:
        return jsonify({"error": "Story not found"}), 404
    return jsonify(story.to_dict()), 200

@story_bp.route('/<int:story_id>/edit', methods=['PUT'])
@jwt_required()
def edit_story(story_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    story = update_story(story_id, data, user_id)
    return jsonify({"message": "Story updated successfully", "story": story.to_dict()}), 200

@story_bp.route('/<int:story_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_story_route(story_id):
    delete_story(story_id)
    return jsonify({"message": "Story deleted successfully"}), 200
