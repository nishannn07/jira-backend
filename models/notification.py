from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Notification(db.Model, TimestampMixin):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="notifications")
