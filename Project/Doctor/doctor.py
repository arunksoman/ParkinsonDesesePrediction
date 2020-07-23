from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, current_user
from ..Models.models import *
import time
from random import uniform
from ..configurations import *
from werkzeug.utils import secure_filename

doctor = Blueprint('doctor', __name__, template_folder='doctor_templates',static_folder='doctor_static',url_prefix='/Doctor')

@doctor.route('/ajaxPlace/<did>')
def ajaxPlace(did):
    places = Place.query.filter_by(district_id=did).join(District).all()
    return render_template("Ajaxplace.html", places=places)

@doctor.route('/doctor_homepage')
@login_required
# @roles_required('doctor')
def doctor_homepage():
    doctor = DoctorDetails.query.filter_by(doctor_id=current_user.id).first()
    if not doctor:
        flash("Please add details of you, So that we can verify you. Unless you can't become part of this initiative.")
    
    return render_template('doc_index.html', name=current_user.username)

@doctor.route('/add_details', methods=["GET", "POST"])
def doctor_details():
    if request.method == "POST":
        place_id = request.form.get("slct_place")
        hospital_id = request.form.get("slct_hospital")
        gender = request.form.get("rdb_gender")
        address = request.form.get("txt_address")
        contact = request.form.get("txt_contact")
        file = request.files['file']
        specialization_id = request.form.get("slct_specialization")
        department_id = request.form.get("slct_department")
        licence_no = request.form.get("txt_licence")
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_name, file_ext = os.path.splitext(file.filename)
            new_filename = file_name + time.strftime("%Y-%I-%M-%S") + str(uniform(0, 1000)).zfill(5) + file_ext
            file.filename = new_filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        add_details = DoctorDetails(place_id=place_id, doctor_id=current_user.id, doctor_gender=gender, 
                                    doctor_address=address, doctor_contact=contact, doctor_image=file.filename, hospital_id=hospital_id, 
                                    doctor_specialization=specialization_id, doctor_department=department_id, doctor_registration=licence_no)
        db.session.add(add_details)
        db.session.commit()
    districts = District.query.all()
    hospitals = Hospital.query.all()
    specializations = Specialization.query.all()
    departments = Department.query.all()
    return render_template("doc_details.html", districts=districts, name=current_user.username, hospitals=hospitals, specializations=specializations, departments=departments)

@doctor.route('/editProfile', methods=["GET", "POST"])
def doctorEditProfile():
    if request.method == "POST":
        new_filename = ""
        name = request.form.get("txt_name")
        email = request.form.get("txt_email")
        district = request.form.get("slct_district")
        place = request.form.get("slct_place")
        gender = request.form.get("rdb_gender")
        address = request.form.get("txt_address")
        contact = request.form.get("txt_contact")
        hospital_id = request.form.get("slct_hospital")
        specialization_id = request.form.get("slct_specialization")
        department_id = request.form.get("slct_department")
        file = request.files['file']
        print(request.files)
        if file.filename != "":
            if file and allowed_file(file.filename):
                file_name, file_ext = os.path.splitext(file.filename)
                new_filename = file_name + time.strftime("-%Y-%I-%M-%S-") + str(uniform(0, 1000)).zfill(5) + file_ext
                file.filename = new_filename
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        else:
            print("hai")
            new_filename = request.form.get("hfile")
        
        update_user = Users.query.filter_by(id=current_user.id).first()
        update_user.username = name
        update_user.email = email
        db.session.commit()
        update_doctorDetails = DoctorDetails.query.filter_by(doctor_id=current_user.id).first()
        update_doctorDetails.place_id = place
        update_doctorDetails.doctor_gender = gender
        update_doctorDetails.doctor_address = address
        update_doctorDetails.doctor_contact = contact
        update_doctorDetails.doctor_image = new_filename
        update_doctorDetails.hospital_id = hospital_id
        update_doctorDetails.doctor_specialization = specialization_id
        update_doctorDetails.doctor_department = department_id
        db.session.commit()
        return redirect(url_for("doctor.doctorEditProfile"))
        
    doctor = Users.query.filter_by(id=current_user.id).first()
    doctor_details = DoctorDetails.query.join(Place, Place.id==DoctorDetails.place_id).join(District, District.id==Place.district_id).add_columns(Place.id, District.id, Place.place_name, District.district_name).filter(DoctorDetails.doctor_id==current_user.id).first()
    if not doctor_details:
        return render_template("enter_details.html")
    district = District.query.all()
    places = Place.query.filter(Place.id==DoctorDetails.place_id).all()
    hospitals = Hospital.query.all()
    specializations = Specialization.query.all()
    departments = Department.query.all()
    return render_template("doc_edit_profile.html", doctor=doctor, doctor_details=doctor_details, districts=district, departments=departments,
                            places=places, name=current_user.username, hospitals=hospitals, specializations=specializations)
