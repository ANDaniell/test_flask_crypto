from flask_admin import Admin
from server.admin.forms import DashBoardView, MyView
from server.models import User, Tag, Post, Message, Comment



def create_admin(app, db):
    admin = Admin(app, name='С нами бог... И помните не слова по русски', template_mode='bootstrap4',
                  index_view=DashBoardView())
    admin.add_view(MyView(User, db.session, name='Пользователи данного аккаунта'))
    admin.add_view(MyView(Tag, db.session, name='Tags'))
    admin.add_view(MyView(Post, db.session, name='Posts'))
    admin.add_view(MyView(Message, db.session, name='Messages'))
    admin.add_view(MyView(Comment, db.session, name='Comments'))

