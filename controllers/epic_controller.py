from models.epic import Epic
from models.project import Project
from models import db
from datetime import datetime

def create_epic(data, user_id):
    epic = Epic(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "open"),
        priority=data.get("priority", "medium"),
        start_date=datetime.strptime(data.get("start_date"), "%Y-%m-%d").date() if data.get("start_date") else None,
        end_date=datetime.strptime(data.get("end_date"), "%Y-%m-%d").date() if data.get("end_date") else None,
        project_id=data.get("project_id")
    )
    db.session.add(epic)
    db.session.commit()
    return epic

def get_epics_by_project(project_id):
    return Epic.query.filter_by(project_id=project_id, is_deleted=False).all()

def get_epic_by_id(epic_id):
    return Epic.query.filter_by(id=epic_id, is_deleted=False).first()

def update_epic(epic_id, data, user_id):
    epic = Epic.query.get_or_404(epic_id)
    
    epic.title = data.get("title", epic.title)
    epic.description = data.get("description", epic.description)
    epic.status = data.get("status", epic.status)
    epic.priority = data.get("priority", epic.priority)
    
    if "start_date" in data:
        epic.start_date = (
            datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            if data["start_date"] else None
        )
    
    if "end_date" in data:
        epic.end_date = (
            datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            if data["end_date"] else None
        )
    
    db.session.commit()
    return epic

def delete_epic(epic_id):
    epic = Epic.query.get_or_404(epic_id)
    epic.is_deleted = True
    db.session.commit()
