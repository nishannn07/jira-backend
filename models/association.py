from sqlalchemy import Table, Column, Integer, ForeignKey
from . import db
user_role_association = Table(
    'user_role',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)
user_project_association = Table(
    'user_project',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)
team_user_association = Table(
    'team_user',
    db.metadata,
    Column('team_id', Integer, ForeignKey('teams.team_id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


project_team_association = Table(
    'project_team',
    db.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('team_id', Integer, ForeignKey('teams.team_id'))
)
