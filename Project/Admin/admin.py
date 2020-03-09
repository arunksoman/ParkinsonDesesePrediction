from flask import Blueprint, render_template, session, request, url_for, redirect, flash, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import numpy as np
import cv2
import glob
# from model import *
import base64

base_dir = os.path.abspath(os.path.dirname(__file__))

admin_blueprint = Blueprint('admin_blueprint', __name__,template_folder='ad_template', url_prefix='/admin')

def save(encoded_data, filename):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2.imwrite(filename, img)

@admin_blueprint.route('/DatasetPrep')
def for_no_method():
    return render_template('datasetprep.html')

@admin_blueprint.route('/DatasetPrep', methods=['POST'])
def Dataset():
    image_from_canvas = request.get_json()
    base_64_image = image_from_canvas['base64']
    base_64_image = base_64_image.split(',')[1]
    
    label = image_from_canvas['label']
    print(base_64_image)
    print(label)
    join_dataset_dir = os.path.join(base_dir, 'Dataset')
    path_for_save = os.path.join(join_dataset_dir, label)
    if not os.path.exists(path_for_save):os.mkdir(path_for_save)
    file_name_finder = glob.glob(path_for_save + '/*.png')
    print(file_name_finder)
    if len(file_name_finder) == 0: 
        file_name = 0
    else:
        file_name = len(file_name_finder)
    file_name = str(file_name).zfill(3) + '.png'
    actual_file_path = os.path.join(path_for_save, file_name)
    print(actual_file_path)
    print("Path_for_save: ", path_for_save)
    save(base_64_image, actual_file_path)
    return render_template('datasetprep.html')