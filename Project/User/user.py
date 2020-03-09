from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import login_required, current_user, roles_required
from flask_login import logout_user
# from model import *

user = Blueprint('user', __name__,template_folder='user_templates',static_folder='static',url_prefix='/User')

@user.route('/user_homepage')
@login_required
# @roles_required('User')
def user_homepage():
    return render_template('user_index.html', name=current_user.username)