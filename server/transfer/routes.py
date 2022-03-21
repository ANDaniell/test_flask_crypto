from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_required

from server import db
from server.models import Post
from server.transfer.forms import PostForm

post = Blueprint('post_blueprint', __name__)


@post.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Transaction was successful')
        return redirect(url_for('main_blueprint.index'))
    return render_template('post.html', form=form, legend="Transaction", title="Transaction")
