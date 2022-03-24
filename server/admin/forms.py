from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from server.models import User, Post


class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role


class DashBoardView(AdminIndexView):
    @expose('/admin', methods=['GET', 'POST'])
    def add_data_db(self):
        all_users = User.query.all()
        all_posts = Post.query.all()
        return self.render('admin/dashboard_index.html', all_users=all_users, all_posts=all_posts)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role

