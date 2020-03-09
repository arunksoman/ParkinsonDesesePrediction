from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import login_required, current_user, roles_required
from flask_login import logout_user
# from model import *

doctor = Blueprint('doctor', __name__,template_folder='doctor_templates',static_folder='static',url_prefix='/doctor')

@doctor.route('/doctor_homepage')
@login_required
# @roles_required('doctor')
def doctor_homepage():
    return render_template('doctor_homepage.html', name=current_user.username)