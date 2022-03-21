from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy import func
import datetime
from sqlalchemy import Column, Integer, DateTime

from server import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Head(db.Model):
    __tablename__ = "heads"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    users = db.relationship('User', backref='head_user', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='recepient', lazy=True)
    tags = db.relationship('Tag', backref='head_tag', lazy=True, cascade="all, delete-orphan")


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    tags = db.relationship('Tag', backref='user_tag', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='author', lazy=True)


    last_name = db.Column(db.String(20), unique=False, nullable=True)
    city = db.Column(db.String(20), unique=False, nullable=True)
    address = db.Column(db.String(20), unique=False, nullable=True)
    country = db.Column(db.String(30))
    phone = db.Column(db.String(20), unique=False, nullable=True)
    state = db.Column(db.String(20), unique=False, nullable=True)
    zip = db.Column(db.String(20), unique=False, nullable=True)


    role = db.Column(db.Boolean, default=False)

    messages = db.relationship('Message', backref='recipient', lazy=True)

    head_id = db.Column(db.Integer, db.ForeignKey('heads.id'), nullable=True)

    def set_password(self, password, hashed_password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return check_password_hash(self.hashed_password,password)

    def __repr__(self):
        return f"User({self.username},{self.email},{self.password})"

class Post(db.Model):  # транзакции
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.Text(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    tags = db.relationship('Tag', backref='post_tag', lazy=True, cascade="all, delete-orphan")
    date_posted = db.Column(db.DateTime, default=func.now())
    head_id = db.Column(db.Integer, db.ForeignKey('heads.id'), nullable=True)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(200), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

    currency = db.Column(db.Text(200))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    head_id = db.Column(db.Integer, db.ForeignKey('heads.id'), nullable=True)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    #created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_date = db.Column(db.DateTime, default=func.now())
    category = db.Column(db.Text(20), nullable=True)
    content = db.Column(db.Text(260), nullable=False)
    topic = db.Column(db.Text(20), nullable=False)
    status = db.Column(db.Boolean, default=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commets = db.relationship('Comment', backref='comments', lazy=True)
    role = db.Column(db.Boolean, default=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text(260), nullable=False)
    reply = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    role = db.Column(db.Boolean, default=False)



