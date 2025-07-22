from models.team import Team
from models.user import User
from models import db

def create_team(data):
    team_name = data.get("team_name")
    description = data.get("description", "")
    member_ids = data.get("member_ids", [])

    team = Team(team_name=team_name, description=description)

    if member_ids:
        members = User.query.filter(User.id.in_(member_ids)).all()
        team.members.extend(members)

    db.session.add(team)
    db.session.commit()
    return team

def get_all_teams():
    return Team.query.all()
