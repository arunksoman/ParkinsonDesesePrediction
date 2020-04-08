from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify, Response
from flask_login import logout_user, login_required, current_user
import numpy as np
import cv2
import glob
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin
from Project import db, app
from ..configurations import *
from ..Models.models import *
import split_folders
import base64

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            user = Users.query.filter_by(id=current_user.id).first()
            if user.roles[0].name == 'Admin':
                return True
            else:
                return False
admin = Admin(name='Project', index_view=MyAdminIndexView(), template_mode='bootstrap3')
class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            user = Users.query.filter_by(id=current_user.id).first()
            if user.roles[0].name == 'Admin':
                return True
            else:
                return False
        # return current_user.is_authenticated and not current_user.is_anonymous

class AdminBaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            user = Users.query.filter_by(id=current_user.id).first()
            # print(user.roles[0].name)
            if user.roles[0].name == 'Admin':
                return True
            else:
                return False
        # return current_user.is_authenticated and not current_user.is_anonymous


adminNew_blueprint = Blueprint('adminNew_blueprint', __name__, template_folder='ad_template', url_prefix='/admin')


def save(encoded_data, filename):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2.imwrite(filename, img)

def split_dataset():
    OUTPUT_DIR = os.path.join(ADMIN_DIR, "Output")
    split_folders.ratio(DATASET_DIR, output=OUTPUT_DIR, seed=1337, ratio=(.8, .2))

@adminNew_blueprint.route('datasetprep/SaveData', methods=['POST'])
def Dataset():
    image_from_canvas = request.get_json()
    base_64_image = image_from_canvas['base64']
    base_64_image = base_64_image.split(',')[1]
    
    label = image_from_canvas['label']
    # print(base_64_image)
    # print(label)
    join_dataset_dir = os.path.join(ADMIN_DIR, 'Dataset')
    path_for_save = os.path.join(join_dataset_dir, label)
    if not os.path.exists(path_for_save):os.mkdir(path_for_save)
    file_name_finder = glob.glob(path_for_save + '/*.png')
    # print(file_name_finder)
    if len(file_name_finder) == 0: 
        file_name = 0
    else:
        file_name = len(file_name_finder)
    file_name = str(file_name).zfill(3) + '.png'
    actual_file_path = os.path.join(path_for_save, file_name)
    # print(actual_file_path)
    # print("Path_for_save: ", path_for_save)
    save(base_64_image, actual_file_path)
    return "success", 200

class LoginadminView(ModelView):
    def is_accessable(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("guest.login"))
class CustomDistrictView(AdminModelView):
    form_columns = ['district_name']

class CustomPlaceView(AdminModelView):
    form_columns = ['place_name', 'Choose District']

class CustomSpecialization(AdminModelView):
    form_columns = ['specialization_name']

class DatasetPrep(AdminBaseView):
    @expose('/')
    def preprocess_dataset(self):
        return self.render('admin/datset_prep.html', endpoint='test')

class MakeTrainTestSplit(AdminBaseView):
    @expose('/')
    def preprocess_dataset(self):
        split_dataset()
        return self.render('admin/success.html', endpoint='test')

class LogoutAdmin(AdminBaseView):
    @expose('/')
    def logoutAdmin(self):
        return redirect(url_for("main.logout"))

admin.add_view(CustomDistrictView(District,db.session))
admin.add_view(CustomPlaceView(Place,db.session))
admin.add_view(CustomSpecialization(Specialization, db.session))
admin.add_view(AdminModelView(Department, db.session))
admin.add_view(AdminModelView(Hospital, db.session))

admin.add_view(DatasetPrep(name='Dataset Preparation'))
admin.add_view(MakeTrainTestSplit(name='Make Train Test split'))
admin.add_view(LogoutAdmin(name='Logout'))
