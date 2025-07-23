from models.project import Project
from models.user import User
from models.task import Task
from models.team import Team
from models import db
from sqlalchemy import func
from datetime import date
from models.activity_log import ActivityLog
from sqlalchemy.orm import joinedload
def create_project(data, user_id):
    project = Project(
        project_name=data.get("project_name"),
        description=data.get("description"),
        project_link=data.get("project_link"),
        status=data.get("status", "active")
    )
    db.session.add(project)
    db.session.commit()
    for tid in data.get("teams", []):
        team = Team.query.get(tid)
        if team:
            project.teams.append(team)
            for member in team.members:
                if member not in project.users:
                    project.users.append(member)

    creator = User.query.get(user_id)
    if creator and creator not in project.users:
        project.users.append(creator)


    db.session.commit()
    return project



def update_project(project_id, data):
    project = Project.query.get_or_404(project_id)
    project.project_name = data.get("project_name")
    project.project_key = data.get("project_key", "").upper()
    project.description = data.get("description")
    project.project_link = data.get("project_link")
    project.status = data.get("status", "active")

    project.teams.clear()
    for tid in data.get("teams", []):
        team = Team.query.get(tid)
        if team:
            project.teams.append(team)

    db.session.commit()
    return project


def get_user_projects(user_id):
    user = User.query.get(user_id)
    if not user:
        return []
    v_projects = set()
    # for project in user.projects:
    #     v_projects.add(project)
    for team in user.teams:
        for project in team.projects:
            if not project.is_deleted:
                v_projects.add(project)
    return sorted(list(v_projects), key=lambda p: p.id)


def get_project_with_stats(project_id):
    project = Project.query.filter_by(id=project_id, is_deleted=False).first_or_404()
    task_stats = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).filter_by(project_id=project_id, is_deleted=False).group_by(Task.status).all()

    stats = {status: count for status, count in task_stats}
    total_tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).count()
    overdue_tasks = Task.query.filter(
        Task.project_id == project_id,
        Task.is_deleted == False,
        Task.due_date < date.today(),
        Task.status != 'done'
    ).count()
    print(total_tasks)
    stats['total'] = total_tasks
    stats['overdue'] = overdue_tasks

    return project, stats


def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.is_deleted = True
    db.session.commit()


def get_all_projects():
    return Project.query.filter_by(is_deleted=False).all()


def update_project_status(user_id, project_id, data):
    project = Project.query.get_or_404(project_id)
    old_status = project.status
    new_status = data.get('status')
    if old_status != new_status:
        project.status = new_status
        db.session.commit()
        log_activity(user_id, project_id, 
                     'status_changed',
                     f'{project.project_name} project status changed from {old_status} to {new_status}')

def get_all_projects_with_teams():
    """
    Fetches all projects and eagerly loads their associated teams.
    This is for the super admin view.
    """
    return Project.query.options(joinedload(Project.teams)).filter(Project.is_deleted==False).all()

def log_activity(user_id, project_id, action, description):
    activity = ActivityLog(
        user_id=user_id,
        project_id=project_id,
        action=action,
        description=description
    )
    db.session.add(activity)
    db.session.commit()