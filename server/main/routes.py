from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from server.models import check_password_hash
from server import bcrypt
from server.main.forms import LoginForm
from server.models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # next_page = url_for('main.account')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
            # return render_template('index.html', title='Account', current_user=current_user)  # TODO поменять на кабинет
    return render_template('login.html', form_login=form, title='Login', legend='Login')


@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('index.html', title='Account', current_user=current_user)  # TODO поменять на кабинет


@main.route('/account', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url_for('main.index'))