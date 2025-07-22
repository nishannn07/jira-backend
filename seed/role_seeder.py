from models import db
from models.role import Role

import click
from flask.cli import with_appcontext

@click.command('seed-roles')
@with_appcontext
def seed_roles():
    roles = ['admin', 'manager', 'user', 'super_admin',"employee"]

    for role in roles:
        existing = Role.query.filter_by(name=role).first()
        if not existing:
            new_role = Role(name=role, is_active=True)
            db.session.add(new_role)
    
    db.session.commit()
    print("Role table seeded")
