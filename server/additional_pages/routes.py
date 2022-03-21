import os
import random
from flask_login import login_required, current_user
from sqlalchemy import exists, DateTime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import MultiDict
from PIL import Image

from flask import render_template, request, redirect, flash, url_for, Blueprint

from server.additional_pages.forms import CommentsForm
from server.bitcoin.btc_core import gen_address, gen_qr_wallet
from server.functions import get_price
from server.main.settings import MINIMAL_DEPOSIT
from server.models import User, Tag, Comment

additional = Blueprint('additional_blueprint', __name__)


@additional.route('/corporate')
def corporate():
    return render_template('corporate.html')


@additional.route('/fees')
def fees():
    return render_template('fees.html')


@additional.route('/security')
def security():
    return render_template('security.html')


@additional.route('/market')
def market():
    return render_template('market.html')


@additional.route('/wallet')
@additional.route('/balance')
def balance():
    from server import db

    bch = round(MINIMAL_DEPOSIT / get_price('BCH'), 4)
    btc = round(MINIMAL_DEPOSIT / get_price('BTC'), 4)
    ltc = round(MINIMAL_DEPOSIT / get_price("LTC"), 4)
    eth = round(MINIMAL_DEPOSIT / get_price('ETH'), 4)
    try:
        user_id = db.session.query(User).filter(User.email == current_user.email).first().id
        tag_id = db.session.query(Tag).filter(Tag.user_id == user_id).first()
        if tag_id:
            price = tag_id.price / get_price('BTC')
            a = gen_address(tag_id.id)
            print(a)

            gen_qr_wallet(a[0])
            qr = [f'img/{a[0]}.jpg', a[0]]
        else:
            print('else')
            price = 0
            qr = ['img/example.png', 'jabsjbcbsidc']
    except Exception as e:
        print(e)
        price = 0
        qr = ['img/example.png', 'jabsjbcbsidc']
    # print(bch, btc, ltc, eth)
    print(price)
    return render_template('balance.html', bch_deposit=bch, btc_deposit=btc, ltc_deposit=ltc, eth_deposit=eth,
                           price=price, qr_btc=qr)


@additional.route('/about')
def about():
    return render_template('about.html')


@additional.route('/privacy')
def privacy():
    return render_template('privacy.html')


@additional.route('/termofuse')
def termofuse():
    return render_template('termofuse.html')


@additional.route('/affiliate')
def affiliate():
    return render_template('affiliate.html')


@additional.route('/smart')
def smart():
    return render_template('smart.html')


@additional.route('/referral')
def referral():
    return render_template('referral.html')


@additional.route('/faq')
def faq():
    return render_template('faq.html')


@additional.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    from server.additional_pages.forms import SupportForm
    from server.models import Message
    from server import db
    form = SupportForm()
    print('sddddddddddddddd')
    user_id = db.session.query(User).filter(User.email == current_user.email).first().id
    messages = db.session.query(Message).filter(Message.user == user_id)
    tickets = []
    if messages:
        for m in messages:
            gg = int(m.id) * 17 + 4000 + random.randint(0, 127)
            #  2022-03-14 13:05:02.551447
            date = str(m.created_date).split('.')[0]
            status = 'Answer received' if m.status else 'Awaiting Response'
            tickets.append([gg, date, m.category, m.topic, status, m.content, m.id])
    else:
        tickets = False
    if form.validate_on_submit():
        print('message', form.text.data, current_user.id, form.topic.data)
        try:
            message = Message(content=form.text.data, user=user_id, role=False, topic=form.topic.data,
                              category=form.category.data)
            db.session.add(message)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f'error: {e}')

    return render_template('support.html', form=form, email_data=current_user.email, tickets=tickets,
                           c_id=current_user.id)


@additional.route('/reload/<user_name>/<message_id>/<code>/<page>')
def reload(user_name, message_id, code, page):
    redirect(url_for(f'additional_blueprint.{page}', user_name=user_name, message_id=message_id, code=code))


@additional.route('/test/<user_name>/<message_id>/<code>', methods=['GET', 'POST'])
@login_required
def comments(user_name, message_id, code):
    if str(current_user.id) == str(user_name):
        from server.models import Message
        from server import db
        form = CommentsForm()
        message = db.session.query(Message).filter(Message.id == message_id).first()
        ticket = []
        if message:
            gg = code
            date = str(message.created_date).split('.')[0]
            ticket = [gg, date, current_user.email, message.category, message.topic, message.content]

        comments = db.session.query(Comment).filter(Comment.reply == message_id)
        comments_data = []
        if comments:
            for c in comments:
                date = str(c.created_date).split('.')[0]
                content = c.content
                role = c.role
                c_user = c.user
                print()
                comments_data.append([date, content, role, c_user])
        if form.validate_on_submit():
            # print('message', form.text.data, current_user.id, form.topic.data)
            try:
                comment = Comment(content=form.text.data, user=current_user.id, role=False, reply=message_id)
                db.session.add(comment)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f'error: {e}')
            form.text.data = ''
            redirect(url_for('additional_blueprint.reload', user_name=user_name, message_id=message_id, code=code,
                             page='comments'))
        return render_template('support2.html', comments_data=comments_data, message_data=ticket, form=form)
    else:
        print(current_user.id, user_name)
        return redirect(url_for('main_blueprint.index'))


@additional.route('/livetrade')
def livetrade():
    return render_template('livetrade.html')


@additional.route('/exchange')
def exchange():
    return render_template('exchange.html')


@additional.route('/orders')
def orders():
    return render_template('orders.html')


@additional.route('/history')
def history():
    return render_template('history.html')
