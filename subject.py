from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import conn_db
import binascii, os
from datetime import date, timedelta, datetime

bp = Blueprint('subject', __name__, template_folder='../templates', url_prefix='/subject')
# add some change
# add second change
# on subject
# a = a+1
@bp.route('/new')
@login_required
def new():
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    # load existing projects
    cur.execute("select idp, abbr from projects order by update_time DESC")
    projs = []
    for proj in cur:
        projs.append(proj)
    # cur.execute("select idp, abbr from projects where abbr = 'TBD'")
    # proje = cur.fetchone()
    # load existing tests
    # TBD
    return render_template('subject_new.html', projs=projs)


@bp.route('/view/<idr>', methods=['POST', 'GET'])
@login_required
def view_single(idr):
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    # current record
    cur.execute("select *,date_format(record_time,'%Y-%m-%d') as rdate from sub_records where idr=%s", (idr,))
    params = cur.fetchone()
    # historic records
    cur.execute(
        "select idr,date_format(record_time,'%Y-%m-%d') as date,air_250r,air_500r, air_1000r,air_2000r,air_4000r,"
        "air_8000r,air_250l,air_500l,air_1000l,air_2000l,air_4000l,air_8000l,bone_250r,bone_500r, bone_1000r,"
        "bone_2000r,bone_4000r,bone_8000r,bone_250l,bone_500l,bone_1000l,bone_2000l,bone_4000l,bone_8000l from sub_records where ids_rec=%s order by record_time desc",
        (params['ids_rec'],))
    records = cur.fetchall()
    # projects
    cur.execute(
        'select a.idp_proj idp,b.abbr abbr, a.isfinish isfinish,a.payment pay from sub_projects a join projects b '
        'on a.idp_proj=b.idp where a.idr_proj=%s', (idr,))
    projs = cur.fetchall()
    totalpay = 0
    for p in projs:
        totalpay += p['pay']
    # tests
    cur.execute(
        'select b.test_name name from sub_tests a join tests b on a.idt_test=b.idt where a.idr_test=%s', (idr,))
    tests = cur.fetchall()
    # print(params, projs, tests)
    return render_template('subject_view.html', params=params, records=records, projs=projs, tests=tests,
                           totalpay=totalpay)


@bp.route('/view/<idr>/update')
@login_required
def update(idr):
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    # current record
    cur.execute('select * from sub_records where idr=%s', (idr,))
    params = cur.fetchone()
    # historic records
    cur.execute("select idr,date_format(record_time,'%Y-%m-%d') as date from sub_records where ids_rec=%s "
                "order by record_time desc", (params['ids_rec'],))
    records = cur.fetchall()
    # projects
    cur.execute(
        'select a.idp_proj idp,b.abbr abbr, a.isfinish isfinish,a.payment pay from sub_projects a join projects b '
        'on a.idp_proj=b.idp where a.idr_proj=%s', (idr,))
    projs = cur.fetchall()
    # all projects
    cur.execute("select  idp, abbr from projects order by record_time DESC")
    projs_all = cur.fetchall()
    # tests
    cur.execute(
        "select b.test_name name from sub_tests a join tests b on a.idt_test=b.idt where a.idr_test=%s", (idr,))
    tests = cur.fetchall()
    testlist = list()
    for test in tests:
        testlist.append(test['name'])
    return render_template('subject_update.html', params=params, records=records, projs=projs, projs_all=projs_all,
                           testlist=testlist)


@bp.route('/creating', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        conn = conn_db()
        cur = conn.cursor()
        # add new subject id
        while True:
            ids = 'S' + binascii.hexlify(os.urandom(6)).decode()
            cur.execute("select count(*) from sub_ids where ids=%s", (ids,))
            if cur.fetchone()[0] == 0:
                break
        while True:
            idr = 'R' + binascii.hexlify(os.urandom(6)).decode()
            cur.execute("select count(*) from sub_records where idr=%s", (idr,))
            if cur.fetchone()[0] == 0:
                break
        params = newOrupdate(idr, ids, mode='sr')
        # sub ID
        cur.execute('insert into sub_ids values (%s)', (ids,))
        # record
        cur.callproc('insert_sub_records', tuple(params.values()))
        # project
        idp_proj = request.form.get('proj_join')
        if idp_proj != 'unknown':
            cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, idp_proj, 'no', 0))
        # test
        tests = request.form.getlist('tests')
        # print(tests)
        for test in tests:
            cur.execute("select idt from tests where test_name=%s", (test,))
            cur.execute("insert into sub_tests values (%s,%s)", (idr, cur.fetchone()[0]))
        conn.commit()
        return idr
    # return redirect(url_for('projects.new'))


# return render_template('consult/create.html')


@bp.route('/view/<idr>/modifying', methods=('GET', 'POST'))
@login_required
def modify(idr):
    if request.method == 'POST':
        conn = conn_db()
        cur = conn.cursor()
        record_date = date.fromisoformat(request.form.get('record_date'))
        is_latest = str(request.form.get('is_latest'))
        # load existing subject ID
        cur.execute("select ids_rec as ids from sub_records where idr=%s", (idr,))
        ids = cur.fetchone()[0]
        # projectsForm
        finproj = filter(lambda key: key.startswith('finp'), request.form.to_dict())
        projs = list()
        for p in finproj:
            idpi = p[4:]
            projs.append((idpi, request.form.get(p), request.form.get('payp' + idpi)))
        if date.today() > record_date and is_latest == 'yes':
            # new record
            while True:
                idr = 'R' + binascii.hexlify(os.urandom(6)).decode()
                cur.execute("select idr from sub_records where idr=%s", (idr,))
                if not cur.fetchall():
                    break
            params = newOrupdate(idr, ids, mode='r')  # new record
            # record
            cur.callproc('insert_sub_records', tuple(params.values()))
        else:
            params = newOrupdate(idr, ids, mode='n')  # update on existing record
            # record
            cur.callproc('update_sub_records', tuple(params.values()))

        # project
        cur.execute("delete from sub_projects where idr_proj=%s", (idr,))
        for proj in projs:
            cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, proj[0], proj[1], proj[2]))
        # test
        tests = request.form.getlist('tests')
        cur.execute("delete from sub_tests where idr_test=%s", (idr,))
        for test in tests:
            cur.execute("select idt from tests where test_name=%s", (test,))
            cur.execute("insert into sub_tests values (%s,%s)", (idr, cur.fetchone()[0]))
        conn.commit()
        return idr


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'GET':
        idp = request.args.get('idp')
        conn = conn_db()
        cur = conn.cursor()
        cur.execute('delete from projects where idp=%s', (idp,))
        if cur.rowcount == 1:
            conn.commit()
            return 'Success', 200
        elif cur.rowcount > 1:
            abort(400)
        elif cur.rowcount < 1:
            abort(404)


@bp.route('/creating/error')
@login_required
def errorpage():
    e = request.args.get('e')
    if e == 'unable':
        return 'Unable to add new subject'
    if e == 'noname':
        return 'Empty subject name'
    if e == 'success':
        return 'Success'
    # if e == 'nop':
    #     return 'Record not exist'


def addtest(testname, testdesc, conn):
    curx = conn.cursor()
    while True:
        idt = 'T' + binascii.hexlify(os.urandom(6)).decode()
        curx.execute("select idt from tests where idt=%s", (idt,))
        if not curx.fetchall():
            break
    curx.execute("insert into tests values (%s,%s,%s)", (idt, testname, testdesc))
    conn.commit()


def cal_thresh(form):
    thresh = list()
    for fo in form:
        fo = list(map(int, fo))
        for i in range(6):
            fo[i] = fo[i] if fo[i] > -20 else None
            thresh.append(fo[i])
        try:
            ave = sum(fo[1:-1]) / 4
            if ave <= 20:
                level = 'normal'
            elif ave <= 40:
                level = 'mild'
            elif ave <= 55:
                level = 'moderate'
            elif ave <= 70:
                level = 'mod-sev'
            elif ave <= 90:
                level = 'severe'
            else:
                level = 'profound'
        except TypeError:
            ave = None
            level = None
        thresh.append(ave)
        thresh.append(level)
    return tuple(thresh)


def newOrupdate(idr, ids, mode='n'):
    # add new record id
    params = dict()
    cur_time = datetime.now()
    params['idr'] = idr
    if mode == 'sr' or mode == 'r':
        params['ids_rec'] = ids
        params['record_time'] = cur_time
    params['update_time'] = cur_time
    params['subname'] = request.form.get('subname').strip()
    # if empty name
    if not params['subname']:
        abort(400)
    age = int(request.form.get('age'))
    age = age if age > 0 else None
    params['age_record'] = age
    params['age'] = age

    params['phone'] = request.form.get('phone').strip()
    params['gender'] = request.form.get('gender')
    params['attitude'] = request.form.get('attitude')
    params['location'] = request.form.get('location')
    params['spare'] = request.form.get('spare')
    params['sparenote'] = request.form.get('sparenote').strip()
    params['aidwearing'] = request.form.get('aidwearing')
    params['diseases'] = request.form.get('diseases').strip()
    params['comments'] = request.form.get('comments').strip()

    airR = [request.form.get('air_250r'), request.form.get('air_500r'), request.form.get('air_1000r'),
            request.form.get('air_2000r'), request.form.get('air_4000r'), request.form.get('air_8000r')]
    airL = [request.form.get('air_250l'), request.form.get('air_500l'), request.form.get('air_1000l'),
            request.form.get('air_2000l'), request.form.get('air_4000l'), request.form.get('air_8000l')]
    boneR = [request.form.get('bone_250r'), request.form.get('bone_500r'), request.form.get('bone_1000r'),
             request.form.get('bone_2000r'), request.form.get('bone_4000r'), request.form.get('bone_8000r')]
    boneL = [request.form.get('bone_250l'), request.form.get('bone_500l'), request.form.get('bone_1000l'),
             request.form.get('bone_2000l'), request.form.get('bone_4000l'), request.form.get('bone_8000l')]

    params['air_250r'], params['air_500r'], params['air_1000r'], params['air_2000r'], params['air_4000r'], params[
        'air_8000r'], params['air_avgr'], params['air_levelr'], params['air_250l'], params['air_500l'], params[
        'air_1000l'], params['air_2000l'], params['air_4000l'], params['air_8000l'], params['air_avgl'], params[
        'air_levell'], params['bone_250r'], params['bone_500r'], params['bone_1000r'], params['bone_2000r'], params[
        'bone_4000r'], params['bone_8000r'], params['bone_avgr'], params['bone_levelr'], params['bone_250l'], \
    params['bone_500l'], params['bone_1000l'], params['bone_2000l'], params['bone_4000l'], params['bone_8000l'], \
    params['bone_avgl'], params['bone_levell'] = cal_thresh((airR, airL, boneR, boneL))

    params['cause_right'] = request.form.get('cause_right')
    params['cause_left'] = request.form.get('cause_left')
    params['shape_right'] = request.form.get('shape_right')
    params['shape_left'] = request.form.get('shape_left')
    params['immittance_right'] = request.form.get('immittance_right')
    params['immittance_left'] = request.form.get('immittance_left')
    params['speech'] = request.form.get('speech')
    return params
