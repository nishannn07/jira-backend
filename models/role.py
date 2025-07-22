from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import db
from .association import user_role_association

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    users = relationship("User", secondary=user_role_association, back_populates="roles")
