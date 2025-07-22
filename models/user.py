from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import *
from datetime import datetime

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_approved_by_admin = Column(Boolean, default=False)
    is_approved_by_manager = Column(Boolean, default=True)  # Default true for managers
    approval_status = Column(String(20), default='pending')  # pending, approved, rejected
    role_raise_request = Column(String(20), default=None) # None, pending, approved, rejected
    requested_team_id = Column(Integer, db.ForeignKey('teams.team_id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    approved_by_admin_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    approved_by_manager_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    
    roles = relationship("Role", secondary=user_role_association, back_populates="users")
    projects = relationship("Project", secondary=user_project_association, back_populates="users")
    teams = relationship("Team", secondary=team_user_association, back_populates="members")
    requested_team = relationship("Team", foreign_keys=[requested_team_id])
    comments = relationship("Comment", back_populates="user")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    reported_tasks = relationship("Task", foreign_keys="Task.reporter_id", back_populates="reporter")
    notifications = relationship("Notification", back_populates="user")
    logins = relationship("Login", back_populates="user")
    time_logs = relationship("TimeLog", back_populates="user")
    activities = relationship("ActivityLog", back_populates="user")
    admin_approved_users = relationship("User", foreign_keys=[approved_by_admin_id], remote_side=[id])
    manager_approved_users = relationship("User", foreign_keys=[approved_by_manager_id], remote_side=[id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_approved_by_admin": self.is_approved_by_admin,
            "is_approved_by_manager": self.is_approved_by_manager,
            "approval_status": self.approval_status,
            "role_raise_request": self.role_raise_request,
            "requested_team": self.requested_team.team_name if self.requested_team else None,
            "roles": [role.name for role in self.roles]
        }