import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from website import predict_img

views = Blueprint('views', __name__)

# Assuming 'routes.py' is inside a folder named 'website' within your root directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current file (routes.py)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'temp/')
        
        if not os.path.isdir(target):
            os.makedirs(target)
        
        file = request.files['img']  # Assuming 'img' is the name of your file input field
        
        if file:
            filename = file.filename
            file.save(os.path.join(target, filename))
            print("Upload Completed")
        else:
            flash('No file uploaded', 'error')  # Flash an error message if no file is uploaded

    return redirect('/prediction/{}'.format(filename))

@views.route("/prediction/<filename>",methods=["GET","POST"])
def prediction(filename):
    #imported process.py
    x=predict_img(filename) #imported from process file
    return render_template('output.html',results=x)
