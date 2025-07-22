import os
import click
from flask.cli import with_appcontext
from controllers.user_controller import create_super_admin

@click.command('create-super-admin')
@with_appcontext
def create_super_admin_command():
    try:
        username = os.environ.get("USERNAME")
        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")

        if not all([username, email, password]):
            raise ValueError("USERNAME, EMAIL, or PASSWORD not set in environment.")

        create_super_admin(username, email, password)
        click.echo(f'Super admin {username} created successfully!')
    except Exception as e:
        click.echo(f'Error creating super admin: {str(e)}')