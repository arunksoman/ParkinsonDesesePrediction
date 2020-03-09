from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import login_required, current_user, roles_required
from flask_login import login_user, logout_user, login_required
from flask_login import logout_user
from Project.Models.models import *
from datetime import datetime as dt

current_time = dt.now()

guest = Blueprint('guest', __name__,template_folder='guest_templates',static_folder='guest_static',url_prefix='/Guest')


@guest.route('login')
def login():
    return render_template('login.html')

@guest.route('login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()
    # print(user.id)
    
    if not user or not (user.password==password):
        flash('Please check your login details and try again.')
        return redirect(url_for('guest.login')) # if user doesn't exist or password is wrong, reload the page"""
    else:
        if user.roles[0].name == 'User':
            login_user(user, remember=remember)
            return redirect(url_for('user.user_homepage'))
        if user.roles[0].name == 'Doctor':
            login_user(user, remember=remember)
            return redirect(url_for('user.user_homepage'))
@guest.route('signup_user')
def signup_user():
    return render_template('signup_user.html')

@guest.route('signup_doctor')
def signup_doctor():
    return render_template('signup_doctor.html')


@guest.route('signup_user', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('guest.signup-user'))

    ####################################
    ########### Role ###################
    role = Roles.query.filter_by(name='User').first()
    if role:
        user_role = role
    else:
        user_role = Roles(name='User')
        db.session.commit()
    ####################################
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    # new_user = UserRegistration(user_email=email, user_name=name, user_password=generate_password_hash(password, method='sha256'))
    
    new_user = Users(email=email, username=username, password=password,email_confirmed_at=current_time)
    new_user.roles = [user_role,]
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    

    return redirect(url_for('guest.login'))

@guest.route('signup_doctor', methods=['POST'])
def signup_doctor_post():

    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')

    doctor = Users.query.filter_by(email=email).first() # if this returns a doctor, then the email already exists in database

    if doctor: # if a doctor is found, we want to redirect back to signup page so doctor can try again  
        flash('Email address already exists')
        return redirect(url_for('guest.signup-doctor'))

    role = Roles.query.filter_by(name='doctor').first()
    if role:
        doctor_role = role
    else:
        doctor_role = Roles(name='Doctor')
        db.session.commit()

    # create new doctor with the form data. Hash the password so plaintext version isn't saved.
    # new_doctor = doctorRegistration(doctor_email=email, doctor_name=name, doctor_password=generate_password_hash(password, method='sha256'))
    new_doctor = Users(email=email, username=username, password=password,email_confirmed_at=current_time)
    new_doctor.roles = [doctor_role,]
    # add the new doctor to the database
    db.session.add(new_doctor)
    db.session.commit()

    return redirect(url_for('guest.login'))

