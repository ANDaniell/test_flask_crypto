from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from mimesis import Person, Text
from sqlalchemy import func

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'anykey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

person = Person('ru')
text = Text('ru')


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