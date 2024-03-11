from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))  # 'student', 'admin', 'donor'
    # Student-specific relationships
    requests = db.relationship('StudentRequest', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FinancialAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    aid_type = db.Column(db.String(50), nullable=False)  # 'financial_assistance', 'bursary', 'scholarship', 'grant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who created the aid
    # Donor-specific relationships
    responses = db.relationship('DonorResponse', backref='financial_aid', lazy='dynamic')

class StudentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Denied'
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    financial_aid_id = db.Column(db.Integer, db.ForeignKey('financial_aid.id'))  # Link to the financial aid applied for

class DonorResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('student_request.id'))
    response = db.Column(db.String(10))  # 'Approve', 'Deny'
    message = db.Column(db.Text)  # Optional message from the donor
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
