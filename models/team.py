from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import team_user_association, project_team_association

class Team(db.Model, TimestampMixin):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(50), nullable=False)
    description = Column(Text)

    members = relationship("User", secondary=team_user_association, back_populates="teams")
    projects = relationship("Project", secondary=project_team_association, back_populates="teams")
    
    def to_dict(self):
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "description": self.description,
            "members": [{"id": m.id, "username": m.username, "email": m.email} for m in self.members]
        }
