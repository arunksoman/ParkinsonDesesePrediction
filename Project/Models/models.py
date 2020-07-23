from flask_login import UserMixin
from Project import db, app

# Define User data-model

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # Relationships
    roles = db.relationship('Roles', secondary='user_roles')
    doc_details = db.relationship('DoctorDetails', backref='docDetails')
    appoinment_to_doctor = db.relationship('Appoinment', backref='doctor_appointed', foreign_keys= 'Appoinment.doctor_id')
    appoinment_for_user = db.relationship('Appoinment', backref='user_for_appoinment', foreign_keys='Appoinment.user_id')
    details_of_user = db.relationship('User_details', backref='user_details', foreign_keys='User_details.user_id')
    user_test_result = db.relationship('Test_results', backref='test_results', foreign_keys='Test_results.user_id')

# Define the Role data-model
class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(50), nullable=False, unique=True)
    # doctors = db.relationship('DoctorDetails', backref='DoctorDetailsDistrict', foreign_keys='DoctorDetails.district_id')
    # userdetails = db.relationship('User_details', backref='UserDetailsDistrict', foreign_keys='User_details.district_id')
    place_details = db.relationship('Place', backref='Choose District', foreign_keys='Place.district_id')

    def __str__(self):
        return "{}".format((self.district_name))

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'),nullable=False)
    place_name = db.Column(db.String(50), nullable=False)
    
    hospital_place = db.relationship('Hospital', backref='Place', foreign_keys='Hospital.place_id')
    doctors = db.relationship('DoctorDetails', backref='DoctorPlace', foreign_keys='DoctorDetails.place_id')
    userdetails = db.relationship('User_details', backref='UserDetailsPlace', foreign_keys='User_details.place_id')

    def __str__(self):
        return "{}".format((self.place_name))

class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specialization_name = db.Column(db.String(50), unique=True)
    doctor_details = db.relationship('DoctorDetails', backref='DoctorDetailsSpecialization')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), unique=True)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(50), nullable=False)
    hospital_address = db.Column(db.String(50), nullable=False)
    hospital_contact = db.Column(db.String(50), nullable=False)
    hospital_email = db.Column(db.String(50), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'),nullable=False)
    hospital_of_doctor = db.relationship('DoctorDetails', backref='doctorDetails', foreign_keys='DoctorDetails.hospital_id')

class DoctorDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'),nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    doctor_gender = db.Column(db.String(150), nullable=False)
    doctor_address = db.Column(db.String(150), nullable=False)
    doctor_contact = db.Column(db.String(50), nullable=False)
    doctor_specialization = db.Column(db.Integer, db.ForeignKey('specialization.id'),nullable=False)
    doctor_department = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=False)
    doctor_registration = db.Column(db.String(50), nullable=False)
    doctor_image = db.Column(db.String(150), nullable=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'),nullable=False)
    doctor_status = db.Column(db.Integer, default=0)

class Appoinment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.String(50), nullable=False)
    appoinment_date = db.Column(db.String(50), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appoinment_status = db.Column(db.Integer, nullable=False, default=0)

class User_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'),nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(150), nullable=True)

class Test_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_img_name = db.Column(db.String(150), nullable=False, unique=True)
    test_result = db.Column(db.String(150), nullable=False)

