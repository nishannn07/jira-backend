# controllers/task_controller.py
from models.task import Task
from models.project import Project
from models.user import User
from models.notification import Notification
from models.comment import Comment
from models.time_log import TimeLog
from models.activity_log import ActivityLog
from models import db
from datetime import datetime

def create_task(data, user_id):
    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        work_type=data.get("work_type"),
        priority=data.get("priority", "low"),
        status=data.get("status", "todo"),
        assigned_to=data.get("assigned_to") or None,
        project_id=data.get("project_id"),
        story_id=data.get("story_id") or None,
        due_date=datetime.strptime(data.get("due_date"), "%Y-%m-%d").date() if data.get("due_date") else None,
        estimated_hours=data.get("estimated_hours"),
        story_points=data.get("story_points"),
        reporter_id=user_id
    )
    db.session.add(task)
    
    db.session.commit()
    log_activity(user_id, task.id, task.project_id, 'created', f'Task "{task.title}" created')
    return task


VALID_STATUSES = ['todo', 'in_progress', 'in_review', 'done']

def update_task(task_id, data, user_id):
    task = Task.query.get_or_404(task_id)
    old_status = task.status
    old_assignee = task.assigned_to
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.work_type = data.get("work_type", task.work_type)
    task.priority = data.get("priority", task.priority)

    new_status = data.get("status", task.status)
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    task.status = new_status

    task.assigned_to = data.get("assigned_to", task.assigned_to)

    if "due_date" in data:
        task.due_date = (
            datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            if data["due_date"] else None
        )

    task.estimated_hours = data.get("estimated_hours", task.estimated_hours)
    task.story_points = data.get("story_points", task.story_points)

    db.session.commit()

    if old_status != task.status:
        log_activity(
            user_id, task.id, task.project_id,
            'status_changed',
            f'Status changed from {old_status} to {task.status}'
        )

    if old_assignee != task.assigned_to:
        old_name = User.query.get(old_assignee).username if old_assignee else 'Unassigned'
        new_name = User.query.get(task.assigned_to).username if task.assigned_to else 'Unassigned'
        log_activity(
            user_id, task.id, task.project_id,
            'assigned',
            f'Assignee changed from {old_name} to {new_name}'
        )

    return task


def get_tasks_by_user(user_id):
    return Task.query.filter_by(assigned_to=user_id, is_deleted=False).all()

def get_tasks_by_project_id(p_id):
    return Task.query.filter_by(project_id=p_id, is_deleted=False).all()

def get_task_with_details(task_id):
    return Task.query.filter_by(id=task_id, is_deleted=False).first()

def add_comment(task_id, content, user_id):
    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    task = Task.query.get(task_id)
    log_activity(user_id, task_id, task.project_id, 'commented', 'Added a comment')
    return comment

def log_time(task_id, hours, description, work_date, user_id):
    if isinstance(work_date, str):
        if not work_date.strip():
            raise ValueError("work_date is required and cannot be empty.")
        try:
            work_date = datetime.strptime(work_date, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid work_date format: {work_date}. Expected format: YYYY-MM-DD") from e


    time_log = TimeLog(
        task_id=task_id,
        user_id=user_id,
        hours_spent=hours,
        description=description,
        work_date=work_date
    )
    db.session.add(time_log)
    db.session.commit()

    task = Task.query.get(task_id)
    log_activity(user_id, task_id, task.project_id, 'time_logged', f'Logged {hours} hours')

    return time_log

def log_activity(user_id, task_id, project_id, action, description):
    activity = ActivityLog(
        user_id=user_id,
        task_id=task_id,
        project_id=project_id,
        action=action,
        description=description
    )
    db.session.add(activity)
    db.session.commit()

def get_project_tasks_by_status(project_id):
    tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).all()
    task_board = {'todo': [], 'in_progress': [], 'in_review': [], 'done': []}
    for task in tasks:
        if task.status in task_board:
            task_board[task.status].append(task)
    return task_board

def search_tasks(query, user_id):
    user = User.query.get(user_id)
    project_ids = [p.id for p in user.projects]
    
    tasks = Task.query.filter(
        Task.project_id.in_(project_ids),
        Task.is_deleted == False,
        Task.title.contains(query)
    ).all()
    
    return tasks

def get_comment_by_task_id(task_id):
    comments = Comment.query.filter_by(task_id = task_id).all()
    return comments

def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "work_type": task.work_type,
        "priority": task.priority,
        "status": task.status,
        "assigned_to": {
            "id": task.assigned_to,
        } if task.assigned_to else None,
        "project_id": task.project_id,
        "project_name": Project.query.get(task.project_id).project_name if Project.query.get(task.project_id) else "",
        "story_id": task.story_id,
        "story_title": task.story.title if task.story else None,
        "due_date": str(task.due_date) if task.due_date else None,
        "estimated_hours": task.estimated_hours,
        "story_points": task.story_points,
        "reporter_id": task.reporter_id
    }


Task.to_dict = task_to_dict


def comment_to_dict(comment):
    return {
        "id": comment.id,
        "task_id": comment.task_id,
        "posted_by": {
            'name': User.query.get(comment.user_id).username,
            'email' : User.query.get(comment.user_id).email
        },
        "content": comment.content,
        "posted_at": str(comment.created_at)
    }

Comment.to_dict = comment_to_dict


def time_log_to_dict(log):
    return {
        "id": log.id,
        "task_id": log.task_id,
        "user_id": log.user_id,
        "hours_spent": log.hours_spent,
        "description": log.description,
        "work_date": str(log.work_date)
    }

TimeLog.to_dict = time_log_to_dict
