from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Epic(db.Model, TimestampMixin):
    __tablename__ = 'epics'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="open", nullable=False)  # open, in_progress, done
    priority = Column(String(50), default="medium", nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="epics")
    stories = relationship("Story", back_populates="epic", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "project_id": self.project_id,
            "stories_count": len(self.stories)
        }
