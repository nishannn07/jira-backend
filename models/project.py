from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import user_project_association, project_team_association

class Project(db.Model, TimestampMixin):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    project_name = Column(String(150), nullable=False)
    project_link = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="active")
    
    users = relationship("User", secondary=user_project_association, back_populates="projects")
    comments = relationship("Comment", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    dashboards = relationship("Dashboard", back_populates="project")
    activities = relationship("ActivityLog", back_populates="project")
    teams = relationship("Team", secondary=project_team_association, back_populates="projects")
    epics = relationship("Epic", back_populates="project")
    stories = relationship("Story", back_populates="project")
    # models/project.py

    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'description': self.description,
            'project_link': self.project_link,
            'status': self.status,
            'teams': [{'team_id': t.team_id, 'team_name': t.team_name} for t in self.teams]
        }
