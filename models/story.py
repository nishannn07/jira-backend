from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Story(db.Model, TimestampMixin):
    __tablename__ = 'stories'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="todo", nullable=False)  # todo, in_progress, in_review, done
    priority = Column(String(50), default="medium", nullable=False)
    story_points = Column(Integer)
    
    epic_id = Column(Integer, ForeignKey('epics.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    epic = relationship("Epic", back_populates="stories")
    project = relationship("Project", back_populates="stories")
    tasks = relationship("Task", back_populates="story")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "story_points": self.story_points,
            "epic_id": self.epic_id,
            "project_id": self.project_id,
            "epic_title": self.epic.title if self.epic else None,
            "tasks_count": len(self.tasks)
        }
