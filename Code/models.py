from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(60),nullable=False,unique=True)
    phone=db.Column(db.String(15),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(250),nullable=False)
    pincode=db.Column(db.String(10),nullable=False)
    blocked=db.Column(db.Boolean,default=False)
   
class Service(db.Model):
    __tablename__="services"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False,unique=True)
    time=db.Column(db.String(25),nullable=False)
    category=db.Column(db.String(20),nullable=False)
    desc=db.Column(db.String(150),nullable=False)
    price=db.Column(db.Float,nullable=False)
    registrations = relationship('Service_Register', backref='service', cascade="all, delete")

class Service_Register(db.Model):
    __tablename__="service_register"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,ForeignKey('users.id'))
    service_id=db.Column(db.Integer,ForeignKey('services.id'))
    user=relationship("User",backref="service_register")

class Service_Request(db.Model):
    __tablename__="service_request"
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,ForeignKey('users.id'))
    professional_id=db.Column(db.Integer,ForeignKey('users.id'))
    service_id=db.Column(db.Integer,ForeignKey('services.id'))
    price=db.Column(db.Float,nullable=False)
    service_date=db.Column(db.Date,nullable=False)
    request_date=db.Column(db.DateTime,default=db.func.now())
    status=db.Column(db.String(20),default="Pending")
    service=relationship('Service',backref="service_request")
    customer=relationship('User',foreign_keys=[customer_id])
    professional=relationship('User',foreign_keys=[professional_id])

def create_tables(app):
    with app.app_context():
        db.create_all()