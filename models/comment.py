from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Comment(db.Model, TimestampMixin):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    
    project = relationship("Project", back_populates="comments")
    user = relationship("User", back_populates="comments")
    task = relationship("Task", back_populates="comments")
