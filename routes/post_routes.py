from flask import render_template, request, redirect, url_for, Blueprint, flash, session, app
post_bp = Blueprint('posts', __name__, url_prefix='/posts')
@post_bp.route('/', methods=['GET'])
def show_dashboard():
    return render_template("index.html")
