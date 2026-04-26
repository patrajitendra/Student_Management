
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    batch = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(200), nullable=True)

    def __init__(self, name, email, roll_number, semester, batch, mobile_number,photo):
        self.name = name
        self.email = email
        self.roll_number = roll_number
        self.semester = semester
        self.batch = batch
        self.mobile_number = mobile_number
        self.photo = photo