# jira_backend-dev-2/routes/team_routes.py

from flask import Blueprint, request, jsonify
from controllers.team_controller import create_team, get_all_teams
from flask_jwt_extended import jwt_required
from rba_decoder import role_required
team_bp = Blueprint('team_bp', __name__, url_prefix='/api/teams')

@team_bp.route('/', methods=['POST'])
@role_required("admin", "super_admin")
@jwt_required()
def create():
    data = request.get_json()
    team = create_team(data)
    return jsonify(team.to_dict()), 201

@team_bp.route('/', methods=['GET'])
@jwt_required()
def get_teams():
    teams = get_all_teams()
    return jsonify([{'team_id': t.team_id, 'team_name': t.team_name} for t in teams]), 200

@team_bp.route('/super-admin/all-teams', methods=['GET'])
@role_required('super_admin')
def get_all_teams_for_super_admin():
    """
    Provides a list of all teams with their members.
    Accessible only by super admins.
    """
    teams = get_all_teams()
    return jsonify([t.to_dict() for t in teams]), 200