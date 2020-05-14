from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin,current_user,login_user,logout_user,LoginManager,login_required
from mtcnn.mtcnn import MTCNN

import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import Normalizer
import joblib


#print("paht is :{}".format(os.getcwd()))
face_net_path = os.getcwd()+"\\flaskblog\\facenet_keras.h5"
model_path = os.getcwd()+"\\flaskblog\\final_model.sav"
face_net = load_model(face_net_path)
model = joblib.load(model_path)
detector = MTCNN()
in_encoder = Normalizer(norm='l2')


app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
loginmanager = LoginManager(app)
from flaskblog import routes


