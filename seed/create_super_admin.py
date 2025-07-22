from controllers.user_controller import create_super_admin
import click
from flask.cli import with_appcontext

@click.command()
@click.option('--username', prompt='Super Admin Username', help='Username for super admin')
@click.option('--email', prompt='Super Admin Email', help='Email for super admin')
@click.option('--password', prompt='Super Admin Password', hide_input=True, help='Password for super admin')
@with_appcontext
def create_super_admin_command(username='Nishan', email='abc@gmail.com', password='pass'):
    try:
        create_super_admin(username, email, password)
        click.echo(f'Super admin {username} created successfully!')
    except Exception as e:
        click.echo(f'Error creating super admin: {str(e)}')

if __name__ == '__main__':
    create_super_admin_command()
