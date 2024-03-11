from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))  # 'student', 'admin', 'donor'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FinancialAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text)
    aid_type = db.Column(db.String(50))  # 'financial_assistance', 'bursary', 'scholarship', 'grant'
    deadline = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class StudentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    financial_aid_id = db.Column(db.Integer, db.ForeignKey('financial_aid.id'))
    message = db.Column(db.Text, nullable=False)  # Message to donors for financial assistance
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Denied'

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('student_request.id'))
    amount = db.Column(db.Float)  # Relevant if donors specify donation amounts
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


