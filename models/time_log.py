from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class TimeLog(db.Model, TimestampMixin):
    __tablename__ = 'time_logs'
    
    id = Column(Integer, primary_key=True)
    hours_spent = Column(Float, nullable=False)
    description = Column(String(500))
    work_date = Column(Date, nullable=False)
    
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    task = relationship("Task", back_populates="time_logs")
    user = relationship("User", back_populates="time_logs")
