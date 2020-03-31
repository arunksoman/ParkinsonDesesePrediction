from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify, Response
from flask_login import login_required, current_user, logout_user
import numpy as np
import cv2
import glob
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from Project import db, app, admin
from ..configurations import *
from ..Models.models import *
import split_folders
import base64

admin_blueprint = Blueprint('admin_blueprint', __name__,template_folder='ad_template', url_prefix='/admin')
admin.add_view(CustomDistrictView(District,db.session))
admin.add_view(CustomSpecialization(Specialization, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Hospital, db.session))

def save(encoded_data, filename):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2.imwrite(filename, img)

def split_dataset():
    OUTPUT_DIR = os.path.join(ADMIN_DIR, "Output")
    split_folders.ratio(DATASET_DIR, output=OUTPUT_DIR, seed=1337, ratio=(.8, .2))

@admin_blueprint.route('datasetprep/SaveData', methods=['POST'])
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

class DatasetPrep(BaseView):
    @expose('/')
    def preprocess_dataset(self):
        return self.render('admin/datset_prep.html', endpoint='test')

class MakeTrainTestSplit(BaseView):
    @expose('/')
    def preprocess_dataset(self):
        split_dataset()
        return self.render('admin/success.html', endpoint='test')
    
admin.add_view(DatasetPrep(name='Dataset Preparation'))
admin.add_view(MakeTrainTestSplit(name='Make Train Test split'))