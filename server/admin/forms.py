from flask import request
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from server.models import User, Post

from flask import render_template, request, redirect, url_for

class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role

'''
    def _handle_view(self, name, **kwargs):
        if not logged_in():
            # делать редирект в некоторых случаях не стоит
            return self.render('admin/login.html')
'''

class DashBoardView(AdminIndexView):
    @expose('/admin', methods=['GET', 'POST'])
    def add_data_db(self):
        all_users = User.query.all()
        all_posts = Post.query.all()
        return self.render('admin/dashboard_index.html', all_users=all_users, all_posts=all_posts)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role

    """
        if current_user.is_authenticated:
            if current_user.role:
                all_users = User.query.all()
                all_posts = Post.query.all()
                return self.render('admin/dashboard_index.html', all_users=all_users, all_posts=all_posts)
                pass
            else:
                return redirect(url_for('main_blueprint.login'))
    """
    '''
if request.method == 'POST':
    frm = request.form.get
    login = frm('login')
    password = frm('pass')

    # проверяете введённые данные...
    if ...
        session.update({обновляете
        сессию})
        session.modified = True
        return self.render('admin/index.html')
    else:
        return self.render('admin/login.html',
                           error=u'Ошиблись паролем?..')
# уже вошёл, но перешёл на /admin/
if logged_in():
    return self.render('admin/index.html')
return self.render('admin/login.html')




'''
