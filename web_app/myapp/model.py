from myapp import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import time, datetime, timedelta
from pytz import timezone as tz
import jwt
from flask_login import current_user
from myapp import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email_address = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    user_count = db.Column(db.Integer, default=0)
    role = db.Column(db.String(30), nullable=False)
    post = db.relationship('Post', back_populates='author', lazy=True)
    
    #last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    

    #polymorphic settings

    user_type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def __init__(self, username, email_address, password, user_count, role):
        self.username = username
        self.email_address = email_address
        self.password = password
        self.user_count = user_count
        self.role = role

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id, 'exp': time() + expires_in
        }, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
class Admin(User):
    __tablename__ = 'admins'
    approve = db.Column(db.Boolean, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __init__(self, username, email_address, password, user_count, role, post=None):
        super().__init__(username, email_address, password, user_count, post, role)
        

    
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id, 'exp': time() + expires_in
        }, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Admin.query.get(id)
class Writer(User):
    __tablename__ = 'writers'
    owned_order = db.relationship('Assignment', back_populates='owner', lazy=True)
    budget = db.Column(db.Integer(), nullable=False, default=0)

    __mapper_args__ = {
        'polymorphic_identity': 'writer'
    }

    def __init__(self, username, email_address, password, user_count, budget, role, post=None):
        super().__init__(username, email_address, password, user_count,budget, post, role)
        
        self.budget = budget


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id, 'exp': time() + expires_in
        }, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Writer.query.get(id)
    
class Student(User):
    __tablename__ = 'students'
    
    
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, email_address, password, user_count, role, post=None):
        super().__init__(username, email_address, password, user_count, post, role)
        

class Editor(User):
    __tablename__ = 'editors'
    __mapper_args__ = {
        'polymorphic_identity': 'editor'
    }

    def __init__(self, username, email_address, password_hash, user_count, role, post=None):
        super().__init__(username, email_address, password_hash, post, user_count, role)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id, 'exp': time() + expires_in
        }, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Student.query.get(id)
    
class Assignment(db.Model, UserMixin):
    __tablename__ = 'assignments'
     
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(30), index=True, unique=True, nullable=False)
    order_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    assignment_type = db.Column(db.String(30), nullable=False)
    academic_level = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow() + timedelta(days=7))
    upload_file = db.Column(db.LargeBinary(255), nullable=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    owner = db.relationship('Writer', back_populates='owned_order', foreign_keys='Assignment.owner_id')

    def __init__(self, title, subject, order_id, pages, word_count, price , description, deadline, assignment_type, academic_level):
        self.title = title
        self.subject = subject
        self.order_id = order_id
        self.pages = pages
        self.word_count = word_count
        self.price = price
        self.assignment_type = assignment_type
        self.academic_level = academic_level
        self.deadline = deadline
        self.description = description
        

    def __repr__(self):
        return f'Asignment {self.subject, self.order_id, self.pages, self.price}'


class Post(db.Model, UserMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    assignment_type = db.Column(db.String(30), nullable=False)
    academic_level = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False, default = datetime.today().strftime("%Y-%m-%d"))
    upload_file = db.Column(db.LargeBinary(255), nullable=True)
    uploaded_file_path = db.Column(db.String(255)) 
    
    


    __mapper_args__ = {
        'polymorphic_identity': 'post'
    }
     
    # Foreign key relationships to link with User and its child classes
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='post', foreign_keys=[user_id])
    
    def __init__(self, title, subject, word_count, description, assignment_type, academic_level, author, deadline):
        self.assignment_type = assignment_type
        self.title = title
        self.subject = subject
        self.word_count = word_count
        self.academic_level = academic_level
        self.description = description
        self.author = author
        self.deadline = deadline

    def get_current_time():
        now = datetime.now(tz(zone='Africa/East Africa')).strftime('%d-%m-%Y, %H:%M:%S')
        return now
        

    def __repr__(self):
        return f"Post('{self.title}', '{self.subject}', '{self.assignment_type}', '{self.academic_level}'"