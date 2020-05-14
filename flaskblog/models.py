from flask_sqlalchemy import SQLAlchemy
from flaskblog import db
from flask_login import UserMixin



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(120), unique=True)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bookinginfo = db.relationship('BookingInfo',backref='booked_info',lazy=True)


    def __repr__(self):
        return "{} {}".format(self.email,self.password)


class BookingInfo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    verified = db.Column(db.String(120))
    pickup = db.Column(db.String(120))
    destination = db.Column(db.String(120))
    driver_email = db.Column(db.String(120))
    date = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "{} {}".format(self.driver_email,self.user_id)


class DriverInfo(db.Model,UserMixin):
    name = db.Column(db.String(50))
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(25),unique=True)
    about = db.Column(db.String(25))
    password = db.Column(db.String(25))
    image = db.Column(db.String(25))
    Age = db.Column(db.Integer)
    Reviews = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    CarNo = db.Column(db.String(50))
    dl = db.Column(db.String(25))
    Address = db.Column(db.String(50))
    Phone = db.Column(db.String(10))
    def __repr__(self):
        return "{} {}".format(self.email,self.password)


