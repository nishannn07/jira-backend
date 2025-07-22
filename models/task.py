from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Task(db.Model, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    work_type = Column(String(50), nullable=False)
    priority = Column(String(50), default="medium", nullable=False)
    summary = Column(Text)
    status = Column(String(50), default="todo", nullable=False)
    due_date = Column(Date)
    estimated_hours = Column(Float)
    story_points = Column(Integer)
    read = Column(Boolean, default=False)
    assigned_to = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    reporter_id = Column(Integer, ForeignKey('users.id'))
    story_id = Column(Integer, ForeignKey('stories.id'), nullable=True)

    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reported_tasks")
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
    time_logs = relationship("TimeLog", back_populates="task")
    activities = relationship("ActivityLog", back_populates="task")
    story = relationship("Story", back_populates="tasks")

    # def task_to_dict(task):
    #     return {
    #         "id": task.id,
    #         "title": task.title,
    #         "description": task.description,
    #         "work_type": task.work_type,
    #         "priority": task.priority,
    #         "status": task.status,
    #         "assigned_to": {
    #             "id": task.assigned_to,

    #         } if task.assigned_to else None,
    #         "project_id": task.project_id,
    #         "due_date": str(task.due_date) if task.due_date else None,
    #         "estimated_hours": task.estimated_hours,
    #         "story_points": task.story_points,
    #         "reporter_id": task.reporter_id
    #     }
