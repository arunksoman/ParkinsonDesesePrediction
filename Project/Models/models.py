from flask_user import UserMixin, UserManager
from Project import db, app, admin
from flask_admin.contrib.sqla import ModelView

# Define User data-model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email_confirmed_at = db.Column(db.DateTime())
    # Relationships
    roles = db.relationship('Roles', secondary='user_roles')
    doc_details = db.relationship('DoctorDetails', backref='docDetails')
    appoinment_to_doctor = db.relationship('Appoinment', backref='doctor_appointed', foreign_keys= 'Appoinment.doctor_id')
    appoinment_for_user = db.relationship('Appoinment', backref='user_for_appoinment', foreign_keys='Appoinment.user_id')

# Define the Role data-model
class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

user_manager = UserManager(app, db, Users)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(50), nullable=False, unique=True)
    hospitals = db.relationship('Hospital', backref='HospitalDistrict')
    doctors = db.relationship('DoctorDetails', backref='DoctorDetailsDistrict')

    def __str__(self):
        return "{}".format((self.district_name))


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
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'),nullable=False)

class DoctorDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'),nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    doctor_address = db.Column(db.String(50), nullable=False)
    doctor_contact = db.Column(db.String(50), nullable=False)
    doctor_specialization = db.Column(db.Integer, db.ForeignKey('specialization.id'),nullable=False)
    doctor_department = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=False)

class Appoinment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appoinment_date = db.Column(db.String(50), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appoinment_status = db.Column(db.Integer, nullable=False, default=0)

class CustomDistrictView(ModelView):
    form_columns = ['district_name']

class CustomSpecialization(ModelView):
    form_columns = ['specialization_name']


