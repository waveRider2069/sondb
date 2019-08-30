import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
# import binascii, os
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


@bp.route('/')
def to_index():
    return redirect(url_for('auth.index'))


@bp.route('/index')
@login_required
def index():
    status_params = {'log': 1, 'notindex': 0, 'notregister': 1, 'user': g.user}
    return render_template('index.html', status_params=status_params)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    status_params = {'log': g.user is not None, 'notindex': 0, 'notregister': 1, 'user': g.user}
    if request.method == 'POST':
        conn = conn_db()
        cur = conn.cursor(buffered=True, dictionary=True)
        # ID = 'sonovaRD'
        # Code = 'abc123'
        username = request.form['username']
        password = request.form['password']
        error = None
        cur.execute("select * from users where binary idu=%s", (username,))
        user = cur.fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['secret'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['idu']
            session.permanent = True
            return redirect(url_for('auth.index'))
        else:
            flash(error)
            return render_template('login_1.html', status_params=status_params)
    return render_template('login_1.html', status_params=status_params)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    status_params = {'log': g.user is not None, 'notindex': 1, 'notregister': 0, 'user': g.user}
    if request.method == 'POST':
        username = request.form['usrid']
        password = request.form['password']
        password1 = request.form['password1']
        invcode = request.form['invcode']
        error = None
        # if empty
        if not username:
            error = 'User ID is required'
        elif not password:
            error = 'Password is required'
        elif not password1:
            error = 'Password confirmation is required'
        elif not invcode:
            error = 'invitation code is required'
        else:
            # verification
            if not verify_char(username, type1='username'):
                error = 'Illegal user ID'
            elif not verify_char(password, type1='password'):
                error = 'Illegal password'
            elif not password == password1:
                error = 'Password input inconsistent'
            else:
                # invitation code / username uniqueness
                conn = conn_db()
                cur = conn.cursor(buffered=True, dictionary=True)
                cur.execute("select idu from users where binary idu=%s", (username,))
                userexist = cur.fetchone()
                cur.execute("select idc from codes where binary idc=%s and maxn>countn", (invcode,))
                validcode = cur.fetchone()
                if userexist:
                    error = f'User {username} is already registered'
                elif not validcode:
                    error = 'Invitation code is invalid'
        if error is None:
            try:
                cur.execute('INSERT INTO users (idu, secret,invcode) VALUES (%s,%s,%s)',
                            (username, generate_password_hash(password), invcode))
                cur.execute("update codes set countn=countn+1 where binary idc=%s", (invcode,))
            except:
                flash('Unknown error when updating database')
                return render_template('register.html', status_params=status_params)
            else:
                conn.commit()
                session.clear()
                flash('Successfully registered! Try log in')
                return redirect(url_for('auth.login'))
        else:
            flash(error)
            return render_template('register.html', status_params=status_params)
    return render_template('register.html', status_params=status_params)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def verify_char(strings, type1):
    if type1 == 'username':
        if len(strings) < 8 or len(strings) > 16:
            return False
    elif type1 == 'password':
        if len(strings) < 8 or len(strings) > 20:
            return False
    else:
        return False
    legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    for s in strings:
        if s not in legal:
            return False
    return True
