from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(150), nullable = False)
    
    tasks = db.relationship('Task', backref='user', lazy = True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable = False, default = 'pendente')
    due_date = db.Column(db.Date, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f'<Task {self.title}>'