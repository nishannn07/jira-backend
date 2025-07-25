from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Login(db.Model):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    password = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="logins")
