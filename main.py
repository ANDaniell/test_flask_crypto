from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func

import email_validator
from flask import flash

from flask_login import current_user, LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField

from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, InputRequired

import os
import shutil
from datetime import datetime

import sqlalchemy
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__name__))
UPLOAD_FOLDER = os.path.join(basedir, 'blog', 'static', 'users')



app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'anykey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

'''
users = Blueprint('users', __name__, template_folder='templates')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)],
                           render_kw={'class': 'form-control'})
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Роли', choices=[('admin', 'admin'), ('user', 'user')])
    submit = SubmitField('Войти')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Это имя уже занято. Пожалуйста, выберите другое', 'danger')
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Этот емайл уже занят. Пожалуйста, введите другой', 'danger')
            raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RequestResetForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash('Нет аккаунта с такой электронной почтой', 'danger')
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    picture = FileField('Изображение (png, jpj)', validators=[FileAllowed(['jpg', 'png']), ])
    user_status = StringField('Статус', validators=[DataRequired(), Length(min=4, max=40)])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('Это имя уже занято. Пожалуйста, выберите другое', 'danger')
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Этот емайл уже занят. Пожалуйста, введите другой', 'danger')
                raise ValidationError('That email is taken. Please choose a different one')



@users.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Ваш аккаунт был создан. Вы можете войти на блог', 'success')
        return redirect(url_for('users.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error))

    return render_template('user/register.html', form_registration=form, title='Регистрация', legend='Регистрация')


@users.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как пользователь {current_user.username}', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
    return render_template('user/login.html', form_login=form, title='Логин', legend='Войти')

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.all()
    users = User.query.all()
    form = UpdateAccountForm()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.user_status.data = current_user.user_status
    elif form.validate_on_submit():
        path_one = os.path.join(os.getcwd(), UPLOAD_FOLDER, user.username)
        path_two = os.path.join(os.getcwd(), UPLOAD_FOLDER, form.username.data)
        os.rename(path_one, path_two)
        current_user.username = form.username.data
        current_user.email = form.email.data

        current_user.user_status = form.user_status.data

        form.picture.data = current_user.image_file

        db.session.commit()
        flash('Ваш аккаунт был обновлён!', 'success')
        return redirect(url_for('users.account'))
    image_file = url_for('static',
                         filename=f'profile_pics' + '/users/' + current_user.username + '/account_img/' +
                                  current_user.image_file)
    return render_template('user/account.html', title='Аккаунт',
                           image_file=image_file, form_update=form, posts=posts, users=users, user=user)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)

    return render_template('user/user_posts.html', title='Общий блог>', posts=posts, user=user)

@users.route('/logout')
def logout():
    current_user.last_seen = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))
'''

@app.get('/')
def index():
    return render_template('index.html')


class Head(db.Model):
    __tablename__ = "heads"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    users = db.relationship('User', backref='head_user', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='recepient', lazy=True)
    tags = db.relationship('Tag', backref='head_tag', lazy=True, cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tags = db.relationship('Tag', backref='user_tag', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='author', lazy=True)

    head_id = db.Column(db.Integer, db.ForeignKey('heads.id'), nullable=True)


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
    username = db.Column(db.String(20), unique=False, nullable=False)
    name = db.Column(db.Text(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)

    head_id = db.Column(db.Integer, db.ForeignKey('heads.id'), nullable=True)


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/any_page/index.html')


class DashBoardView(AdminIndexView):
    @expose('/')
    def add_data_db(self):
        '''
        for i in range(10):
            if not len(User.query.all()) >= 10:
                user = User(username=person.full_name(), email=person.email(), password=person.password())
                db.session.add(user)
                db.session.commit()

                post = Post(title=text.title(), content=text.text(quantity=5))
                post.user_id = user.id
                db.session.add(post)

                comment = Comment(username=user.username, body='Клевая статья. Всем добра', post_id=post.id)
                db.session.add(comment)
            db.session.commit()'''
        all_users = User.query.all()
        all_posts = Post.query.all()
        return self.render('admin/dashboard_index.html', all_users=all_users, all_posts=all_posts)


admin = Admin(app, name='Мой кабинет', template_mode='bootstrap4', index_view=DashBoardView(), endpoint='admin')
admin.add_view(ModelView(User, db.session, name='Пользователи данного аккаунта'))
admin.add_view(ModelView(Post, db.session, name='Транзакции'))
admin.add_view(ModelView(Tag, db.session, name='Рефералки'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
