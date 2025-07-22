from flask import render_template, request, redirect, url_for, Blueprint, flash, jsonify
from controllers.user_controller import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.team import Team
from rba_decoder import *
user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

@user_bp.route('/teams', methods=['GET'])
def get_teams_for_signup():
    teams = Team.query.all()
    return jsonify([{"team_id": t.team_id, "team_name": t.team_name, "description": t.description} for t in teams])
    
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    username = data.get("username")
    lastname = data.get('lastname')
    email = data.get("email")
    password = data.get('password')
    confirm = data.get('confirm')
    role = data.get('role', 'employee') 
    team_id = data.get('team_id')
    
    print(data)
    
    if not username or not lastname or not email or not password or not confirm:
        return jsonify({'msg': 'All fields are required'}), 400
    
    if password != confirm:
        return jsonify({'msg': 'Passwords do not match'}), 400
    
    if get_user_by_username(username):
        return jsonify({"msg": 'Username already exists!'}), 401
    
    if get_user_by_email(email):
        return jsonify({"msg": 'Email already exists!'}), 401

    if role not in ['manager', 'employee']:
        return jsonify({'msg': 'Invalid role selected'}), 400

    if role == 'employee' and not team_id:
        return jsonify({'msg': 'Team selection is required for employees'}), 400
    
    try:
        create_user(username, email, username, lastname, password, role, team_id)
        return jsonify({
            "msg": 'Registration successful! Your account is pending approval. You will be notified once approved.'
        }), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
        

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    print(data)
    email = data.get("email")
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'Missing email or password'}), 400
    user = get_user_by_email(email)
    if user and check_user_password(user, password):
        if not is_user_approved(user):
            return jsonify({'msg': 'Your account is pending approval. Please wait for admin/manager approval.'}), 403
        
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles]
            }
        })
    else:
        return jsonify({'msg': "Invalid email or password"}), 401

@user_bp.route('/me/overview', methods=['GET'])
@jwt_required()
def user_overview():
    user_id = int(get_jwt_identity())
    overview = get_user_overview(user_id)
    
    return jsonify(overview), 200

@user_bp.route('/admin/pending', methods=['GET'])
@role_required("super_admin")
def get_pending_users():
    current_user_id = int(get_jwt_identity())
    current_user = get_user_by_id(current_user_id)
    
    pending_users = get_pending_users_for_admin()
    return jsonify([user.to_dict() for user in pending_users])

@user_bp.route('/admin/approve/<int:user_id>', methods=['POST'])
@role_required("super_admin")
def approve_user_admin(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = get_user_by_id(current_user_id)
    
    try:
        approved_user = approve_user_by_admin(current_user_id, user_id)
        return jsonify({
            'msg': 'User approved successfully',
            'user': approved_user.to_dict()
        })
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400

@user_bp.route('/admin/reject/<int:user_id>', methods=['POST'])
@role_required("super_admin")
def reject_user_admin(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = get_user_by_id(current_user_id)
    
    try:
        rejected_user = reject_user(current_user_id, user_id)
        return jsonify({
            'msg': 'User rejected successfully',
            'user': rejected_user.to_dict()
        })
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400

@user_bp.route('/manager/pending', methods=['GET'])
@role_required("manager", "admin", "super_admin")
def get_pending_employees():
    current_user_id = int(get_jwt_identity())
    current_user = get_user_by_id(current_user_id)
    
    pending_employees = get_pending_employees_for_manager(current_user_id)
    return jsonify([user.to_dict() for user in pending_employees])

@user_bp.route('/manager/approve/<int:employee_id>', methods=['POST'])
@role_required("manager", "admin", "super_admin")
def approve_employee_manager(employee_id):
    current_user_id = int(get_jwt_identity())
    current_user = get_user_by_id(current_user_id)
    
    try:
        approved_employee = approve_employee_by_manager(current_user_id, employee_id)
        return jsonify({
            'msg': 'Employee approved successfully',
            'user': approved_employee.to_dict()
        })
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400

@user_bp.route('/request-role-raise', methods=['POST'])
@jwt_required()
def request_role_raise_route():
    user_id = int(get_jwt_identity())
    try:
        user = request_role_raise(user_id)
        return jsonify({
            'msg': 'Role raise request submitted successfully',
            'user': user.to_dict()
        })
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400

@user_bp.route('/admin/approve-role-raise/<int:user_id>', methods=['POST'])
@role_required("super_admin")
def approve_role_raise_route(user_id):
    current_user_id = int(get_jwt_identity())
    try:
        approved_user = approve_role_raise(current_user_id, user_id)
        return jsonify({
            'msg': 'Role raise approved successfully',
            'user': approved_user.to_dict()
        })
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400

@user_bp.route('/admin/role-raise-requests', methods=['GET'])
@role_required("super_admin")
def get_role_raise_requests():
    requests = get_pending_role_raise_requests()
    return jsonify([user.to_dict() for user in requests])