from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import conn_db
import binascii, os
from datetime import date, timedelta, datetime

bp = Blueprint('projects', __name__, template_folder='../templates', url_prefix='/projects')


@bp.route('/new')
@login_required
def new():
    params = dict()
    today = date.today()
    tomorrow = today + timedelta(days=1)
    params['today'] = today.strftime('%Y-%m-%d')
    params['tomorrow'] = tomorrow.strftime('%Y-%m-%d')
    status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
    return render_template('projects_new.html', params=params, status_params=status_params)


@bp.route('/view/<idp>', methods=['POST', 'GET'])
@login_required
def view_single(idp):
    conn = conn_db()
    cur = conn.cursor()
    user = g.user
    # cur = conn.cursor(buffered=True, dictionary=True)
    # cur.execute('select * from projects where idu_proj=%s and idp=%s', (user, idp))
    # params = cur.fetchone()
    page_state = request.values.get('page_state')

    params = dict()
    cur.callproc('aggregate_single', (user, idp))
    for se in cur.stored_results():
        keys = se.column_names
        for vals in se:
            params = dict(zip(keys, vals))
            # params['budget'] = format(params['budget'], ',')
            # params['totalp'] = format(params['totalp'], ',')
            break  # 1 case
    if params:
        # Beautify budget
        budget = params['budget']
        if budget:
            params['budget'] = format(int(budget), ',')
        # #  Decide if delayed
        # if params['state'] == 'in progress':
        #     endby = date.fromisoformat(str(params['dueto_end']))
        #     today = date.today()
        #     if today > endby:
        #         params['state'] = 'delayed'
        # former page state
        params['page_state'] = page_state
        status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
        return render_template('projects_view.html', params=params, status_params=status_params)
    else:
        return 'Record not exist'


@bp.route('/view/<idp>/search_subs', methods=['GET'])
@login_required
def search_subs_proj(idp):
    params = dict()
    user = g.user
    try:
        params['page'] = abs(int(request.args.get('page')))
    except:
        params['page'] = 1
    # 20 box per page
    boxes = 20
    conn = conn_db()
    cur = conn.cursor()
    # sort
    sort = request.args.get('sort')
    if sort and sort in ['2', '3', '4']:
        params['sort'] = sort
    else:
        params['sort'] = '1'
    params['isfinish'] = request.args.get('isfinish')
    if params['isfinish'] == '0':
        statc = 'no,unfinished'
    else:
        statc = 'yes,finished'
    # call search procedure
    cur.callproc('search_subs_proj', (user, params['sort'], idp, statc))
    reclist, curlist, projs = list(), list(), list()
    # print(params)
    # records information
    for se in cur.stored_results():
        keys = se.column_names
        for vals in se:
            sub = dict(zip(keys, vals))
            sub['idrs'] = sub.get('idrs').split(',')
            sub['rdates'] = sub.get('rdates').split(',')
            if sub.get('idps'):
                sub['idps'] = sub.get('idps').split(',')
                sub['abbrs'] = sub.get('abbrs').split(',')
            else:
                sub['idps'] = []
                sub['abbrs'] = []
            reclist.append(sub)
    # print(reclist)
    # total results number, pages, and range
    params['results'] = len(reclist)
    params['pages'] = int((params['results'] + boxes - 1) / boxes)
    if params['results'] > 0:
        if params['pages'] < params['page']:
            params['page'] = params['pages']
        curlist = reclist[(params['page'] - 1) * boxes:boxes * params['page']]
        # #     projects infomation
        # cur = conn.cursor(dictionary=True, buffered=True)
        # cur.execute(f"select * from projs_search where idr in {tuple(map(lambda rl: rl['idr'], curlist))}")
        # for proj in cur:
        #     projdict[proj['idr']] = {'idps': proj.get('idps').split(','), 'abbrs': proj.get('abbrs').split(',')}
        cur.execute("select idp, abbr from projects where binary idu_proj=%s", (user,))
        projs = cur.fetchall()
    cur.execute("drop table if exists subs_search_proj")
    return render_template('projects_sublist.html', reclist=curlist, params=params, projs=projs)


@bp.route('/view/<idp>/update')
@login_required
def update(idp):
    conn = conn_db()
    user = g.user
    cur = conn.cursor(buffered=True, dictionary=True)
    cur.execute('select * from projects where binary idu_proj=%s and idp=%s', (user, idp))
    params = cur.fetchone()
    if params:
        status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
        return render_template('projects_update.html', params=params, idp=idp, status_params=status_params)
    else:
        return 'Record not exist'


@bp.route('/overview', methods=('GET', 'POST'))
@login_required
def overview():
    return redirect(url_for('projects.changestate', state='all'))


@bp.route('/overview/<state>')
@login_required
def changestate(state):
    conn = conn_db()
    cur = conn.cursor()
    state = state.lower()
    user = g.user
    params_list = list()
    cur.callproc('aggregate', (user, state))
    for se in cur.stored_results():
        keys = se.column_names
        for vals in se:
            proj = dict(zip(keys, vals))
            proj['budget'] = format(proj['budget'], ',')
            proj['totalp'] = format(proj['totalp'], ',')
            params_list.append(proj)
    status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}

    return render_template('projects_overview.html', params_list=params_list, pstate=state, status_params=status_params)


@bp.route('/creating', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        user = g.user
        conn = conn_db()
        cur = conn.cursor()
        title = request.form.get('title')
        abbr = request.form.get('abbr')
        # make sure unique project id/title/abbr
        # error = None
        cur.execute("select title from projects where binary idu_proj=%s and (title=%s or abbr=%s)", (user, title, abbr))
        if cur.fetchall():
            return 'Error: Duplicated title or abbreviation with an existing project'
        else:
            while True:
                idp = 'P' + binascii.hexlify(os.urandom(6)).decode()
                cur.execute("select idp from projects where idp=%s", (idp,))
                if not cur.fetchall():
                    break
            params = dict()
            params['idu_proj'] = user
            params['idp'] = idp
            params['title'] = request.form.get('title').strip()
            params['abbr'] = request.form.get('abbr').strip()
            params['leader'] = request.form.get('leader').strip()
            params['start_time'] = request.form.get('start_time')
            params['dueto_end'] = request.form.get('dueto_end')
            start = date.fromisoformat(params['start_time'])
            endby = date.fromisoformat(params['dueto_end'])
            if start >= endby:
                return 'Error: Ending time precedes starting time'
            params['state'] = 'in progress'
            params['budget'] = request.form.get('budget') or 0
            params['subjectn'] = request.form.get('subjectn') or 0
            params['visits'] = request.form.get('visits') or 0
            params['description'] = request.form.get('description').strip()
            cur_time = datetime.now()
            params['record_time'] = cur_time
            params['update_time'] = cur_time
            # print(tuple(params.values()))
            cur.callproc('insert_projects', tuple(params.values()))
            conn.commit()
            return redirect(url_for('projects.view_single', idp=idp))
    else:
        return 'Error: data not delivered'


@bp.route('/view/<idp>/modifying', methods=('GET', 'POST'))
@login_required
def modify(idp):
    if request.method == 'POST':
        user = g.user
        conn = conn_db()
        cur = conn.cursor()
        title = request.form.get('title')
        abbr = request.form.get('abbr')
        # make sure unique project id/title/abbr
        cur.execute("select title from projects where idp!=%s and binary idu_proj=%s and (title=%s or abbr=%s)",
                    (user, idp, title, abbr))
        if cur.fetchall():
            return 'Error: Duplicated title or abbreviation with an existing project;'
        else:
            params = dict()
            params['idu_proj'] = user
            params['idp'] = idp
            params['title'] = request.form.get('title').strip()
            params['abbr'] = request.form.get('abbr').strip()
            params['leader'] = request.form.get('leader').strip()
            params['start_time'] = request.form.get('start_time')
            params['dueto_end'] = request.form.get('dueto_end')
            params['state'] = request.form.get('state')
            start = date.fromisoformat(params['start_time'])
            endby = date.fromisoformat(params['dueto_end'])
            if start >= endby:
                return 'Error: Ending time precedes starting time'
            params['budget'] = request.form.get('budget') or 0
            params['subjectn'] = request.form.get('subjectn') or 0
            params['visits'] = request.form.get('visits') or 0
            # description = request.form.get('description')
            params['description'] = request.form.get('description').strip()
            cur_time = datetime.now()
            params['update_time'] = cur_time
            # print(tuple(params.values()))
            cur.callproc('update_projects', tuple(params.values()))
            conn.commit()
            return redirect(url_for('projects.view_single', idp=idp))
    else:
        return 'Error: Record not existing'


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'GET':
        user = g.user
        idp = request.args.get('idp')
        conn = conn_db()
        cur = conn.cursor()
        cur.execute('delete from projects where binary idu_proj=%s and idp=%s', (user, idp))
        if cur.rowcount == 1:
            conn.commit()
            return 'Success', 200
        elif cur.rowcount > 1:
            abort(400)
        elif cur.rowcount < 1:
            abort(404)


@bp.route('/delete/error')
@login_required
def errorpage():
    e = request.args.get('e')
    if e == 'more':
        return 'More than one record affected'
    if e == 'nop':
        return 'Record not exist'


def get_post(id, check_author=True):
    post = conn_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post
