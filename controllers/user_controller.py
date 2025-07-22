from models.user import User
from models.login import Login 
from models.role import Role
from models.team import Team
from models import db 
from datetime import datetime
from controllers.project_controller import get_user_projects

def create_user(username, email, first_name, last_name, password, role_name, team_id=None):
    new_user = User(
        username=username, 
        email=email, 
        first_name=first_name, 
        last_name=last_name,
        requested_team_id=team_id if role_name == 'employee' else None
    )
    user_role = Role.query.filter_by(name=role_name).first()
    if not user_role:
        raise ValueError(f"Role {role_name} not found")
    
    new_user.roles.append(user_role)

    if role_name == 'manager':
        new_user.is_approved_by_manager = True
        new_user.approval_status = 'pending_admin' 
    elif role_name == 'employee':
        new_user.is_approved_by_admin = False
        new_user.is_approved_by_manager = False
        new_user.approval_status = 'pending_admin'  
    
    db.session.add(new_user)
    db.session.commit()
    
    new_login = Login(user_id=new_user.id, password=password)
    db.session.add(new_login)
    db.session.commit()
    
    return new_user

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

def get_user_by_id(id):
    user = User.query.get(id)
    return user

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def check_user_password(user, password):
    if not user:
        return False
    login_entry = Login.query.filter_by(user_id=user.id).first()
    if login_entry and login_entry.password == password:
        return True 
    return False

def is_user_approved(user):
    if not user:
        return False
    if any(role.name == 'super_admin' for role in user.roles):
        return True
    if not user.is_approved_by_admin:
        return False
    if any(role.name == 'employee' for role in user.roles):
        return user.is_approved_by_manager
    
    return True

def get_pending_users_for_admin():
    return User.query.filter_by(is_approved_by_admin=False).all()

def get_pending_employees_for_manager(manager_id):
    manager = User.query.get(manager_id)
    if not manager or not any(role.name in ['manager', 'super_admin'] for role in manager.roles):
        return []
    manager_teams = [team.team_id for team in manager.teams]
    
    return User.query.filter(
        User.is_approved_by_admin == True,
        User.is_approved_by_manager == False,
        User.requested_team_id.in_(manager_teams)
    ).all()

def approve_user_by_admin(admin_id, user_id):
    admin = User.query.get(admin_id)
    user = User.query.get(user_id)
    if not admin or not any(role.name == 'super_admin' for role in admin.roles):
        raise ValueError("Only super admin can approve users")
    if not user:
        raise ValueError("User not found")
    
    user.is_approved_by_admin = True
    user.approved_by_admin_id = admin_id
    if any(role.name == 'manager' for role in user.roles) or not user.requested_team_id:
        user.approval_status = 'approved'
        user.approved_at = datetime.utcnow()
    else:
        user.approval_status = 'pending_manager'
    
    db.session.commit()
    return user

def approve_employee_by_manager(manager_id, employee_id):
    manager = User.query.get(manager_id)
    employee = User.query.get(employee_id)
    
    if not manager or not any(role.name in ['manager', 'super_admin'] for role in manager.roles):
        raise ValueError("Only managers can approve employees")
    
    if not employee:
        raise ValueError("Employee not found")
    
    if not employee.is_approved_by_admin:
        raise ValueError("Employee must be approved by admin first")
    manager_team_ids = [team.team_id for team in manager.teams]
    if employee.requested_team_id not in manager_team_ids:
        raise ValueError("Manager cannot approve employee for this team")
    
    employee.is_approved_by_manager = True
    employee.approved_by_manager_id = manager_id
    employee.approval_status = 'approved'
    employee.approved_at = datetime.utcnow()
    
    if employee.requested_team_id:
        team = Team.query.get(employee.requested_team_id)
        if team and employee not in team.members:
            team.members.append(employee)
    
    db.session.commit()
    return employee

def reject_user(admin_id, user_id, reason=""):
    admin = User.query.get(admin_id)
    user = User.query.get(user_id)
    
    if not admin or not any(role.name == 'super_admin' for role in admin.roles):
        raise ValueError("Only super admin can reject users")
    
    if not user:
        raise ValueError("User not found")
    
    user.approval_status = 'rejected'
    db.session.commit()
    return user

def create_super_admin(username, email, password):
    new_user = User(username=username, email=email, is_approved_by_admin=True, is_approved_by_manager=True, approval_status='approved')
    super_role = Role.query.filter_by(name='super_admin').first()
    new_user.roles.append(super_role)
    db.session.add(new_user)
    db.session.commit()
    new_login = Login(user_id=new_user.id, password=password)
    db.session.add(new_login)
    db.session.commit()

def assign_role(username, role):
    user = User.query.filter_by(username=username).first()
    new_role = Role.query.filter_by(name=role).first()
    if new_role not in user.roles:
        user.roles.append(new_role)
        db.session.commit()

def get_all_users():
    users = User.query.all()
    return users

def get_user_overview(user_id):
    user = User.query.get_or_404(user_id)
    # user_projects = [project.to_dict() for project in user.projects]
    user_projects = [project.to_dict() for project in get_user_projects(user_id)]
    user_teams = []
    for team in user.teams:
        user_teams.append({
            "team_id": team.team_id,
            "team_name": team.team_name,
            "description": team.description,
            "members": [{"id": member.id, "username": member.username, "email": member.email} for member in team.members]
        })

    return {
        "projects": user_projects,
        "teams": user_teams
    }

def request_role_raise(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    user.role_raise_request = 'pending'
    db.session.commit()
    return user

def approve_role_raise(admin_id, user_id):
    admin = User.query.get(admin_id)
    user = User.query.get(user_id)
    if not admin or not any(role.name == 'super_admin' for role in admin.roles):
        raise ValueError("Only super admin can approve role raises")
    if not user:
        raise ValueError("User not found")
    
    manager_role = Role.query.filter_by(name='manager').first()
    if not manager_role:
        raise ValueError("Manager role not found")

    if manager_role not in user.roles:
        user.roles.append(manager_role)
    
    user.role_raise_request = 'approved'
    db.session.commit()
    return user

def get_pending_role_raise_requests():
    return User.query.filter_by(role_raise_request='pending').all()