import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import conn_db

bp = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id
        # conn_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        ID = 'sonovaRD'
        Code = 'abc123'
        username = request.form['username']
        password = request.form['password']
        error = None
        if username == ID and password == Code:
            session['user_id'] = username
            session.permanent = True
            # print(username,password)
            return redirect(url_for('auth.index'))
        elif username != ID:
            error = 'Incorrect username'
        elif password != Code:
            error = 'Incorrect password'
        flash(error)
    return render_template('login_1.html')


@bp.route('/')
def to_index():
    return redirect(url_for('auth.index'))
    # return 'abc'

@bp.route('/index')
@login_required
def index():
    return render_template('index.html')


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
