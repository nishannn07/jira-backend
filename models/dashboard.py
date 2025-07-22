from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Dashboard(db.Model, TimestampMixin):
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    dashboard_name = Column(String(150), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="dashboards")
