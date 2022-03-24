from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from server.models import check_password_hash, Tag
from server import bcrypt, db
from server.main.forms import LoginForm, RegistrationForm, ReferralForm, UserDataForm
from server.models import User

main = Blueprint('main_blueprint', __name__)


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            print('login alright')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # next_page = url_for('main.account')
            return redirect(next_page) if next_page else redirect(url_for('main_blueprint.index'))
        else:
            print('login error')
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
            # return render_template('index.html', title='Account', current_user=current_user)  # TODO поменять на кабинет
    return render_template('login.html', form_login=form, title='Login', legend='Login')


@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ReferralForm()
    email = current_user.email
    user_id = db.session.query(User).filter(User.email == email).first().id
    form_user_data = UserDataForm()
    form_user_data.password.data = ''
    print(current_user.city)

    if form.validate_on_submit():
        code = form.code.data
        print(email, code)

        from sqlalchemy.sql import exists
        print(db.session.query(exists().where(Tag.name == code)).scalar())
        try:
            if (db.session.query(exists().where(Tag.name == code)).scalar()):
                tag_id = db.session.query(Tag).filter(Tag.name == code).first().id
                # query = db.session.query(User).filter(User.email == email).update({User.tags: tag_id}, synchronize_session=False)
                query = db.session.query(Tag).filter(Tag.name == code).update({Tag.user_id: user_id},
                                                                              synchronize_session=False)
                # db.session.add(query)
                db.session.commit()
                flash('Your account code add successfully')
            else:
                print('this tag doesnt exist')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f'error: {e}')
    tag = db.session.query(Tag).filter(Tag.user_id == user_id).first()
    if tag:
        boulean_tag = True
    else:
        boulean_tag = False

    if form_user_data.validate_on_submit():
        print("last_name,city")
        try:
            if True:
                # db.session.add(query)
                last_name = form_user_data.last_name.data
                city = form_user_data.city.data
                address = form_user_data.address.data
                country = form_user_data.country.data
                phone = form_user_data.phone.data
                state = form_user_data.state.data
                zip = form_user_data.zip.data

                query = db.session.query(User).filter(User.id == current_user.id).update(
                    {User.last_name: last_name, User.city: city, User.address: address, User.country: country,
                     User.phone: phone, User.state:state, User.zip:zip},
                    synchronize_session=False)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f'error: {e}')

    return render_template('account.html', title='Account', current_user=current_user,
                           form_referral=form, flag=boulean_tag, form_user_data=form_user_data)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))


@main.route('/sing-up', methods=['GET', 'POST'])
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    country=form.country.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account create successfully')
        return redirect(url_for('main_blueprint.login'))
    else:
        flash('Зарегистрироваться не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
    return render_template('register.html', form_registration=form, title='Registration', legend='Registration')
