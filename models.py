from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    def __repr__(self):
        return f"<Client {self.name}>"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100),nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))

    #client = db.relationship('Client', backref='appointments')

    def __repr__(self):
        return f"<Appointment {self.client.name} at {self.starts_at}>"
