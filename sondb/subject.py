from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import conn_db
import binascii, os
from datetime import date, timedelta, datetime

bp = Blueprint('subject', __name__, template_folder='../templates', url_prefix='/subject')


@bp.route('/new')
@login_required
def new():
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    user = g.user
    # load existing projects
    cur.execute("select idp, abbr from projects where binary idu_proj=%s order by update_time DESC", (user,))
    projs = cur.fetchall()
    # load existing tests
    cur.execute("select idt, test_name name, test_desc description,priority from tests order by priority, name")
    tests = cur.fetchall()
    # for proj in cur:
    #     projs.append(proj)
    # cur.execute("select idp, abbr from projects where abbr = 'TBD'")
    # proje = cur.fetchone()
    # load existing tests
    # TBD
    status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
    return render_template('subject_new.html', projs=projs, tests=tests, status_params=status_params)


@bp.route('/view/<idr>', methods=['POST', 'GET'])
@login_required
def view_single(idr):
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    user = g.user
    # current record
    cur.execute(
        "select *,date_format(record_time,'%Y-%m-%d') as rdate from sub_records where binary idu_rec=%s and idr=%s",
        (user, idr))
    params = cur.fetchone()
    if params:
        # historic records
        cur.execute(
            "select idr,date_format(record_time,'%Y-%m-%d') as rdate,air_125r,air_250r,air_500r,air_750r, air_1000r,"
            "air_1500r,air_2000r,air_3000r,air_4000r,air_6000r, air_8000r,air_125l,air_250l,air_500l,air_750l,air_1000l,air_1500l,"
            "air_2000l,air_3000l,air_4000l,air_6000l,air_8000l,bone_125r,bone_250r,bone_500r,bone_750r, bone_1000r,bone_1500r,"
            "bone_2000r,bone_3000r,bone_4000r,bone_6000r, bone_8000r,bone_125l,bone_250l,bone_500l,bone_750l, bone_1000l,"
            "bone_1500l,bone_2000l,bone_3000l,bone_4000l,bone_6000l, bone_8000l from sub_records where ids_rec=%s order by "
            "record_time desc", (params['ids_rec'],))
        records = cur.fetchall()
        # projects
        cur.execute(
            'select a.idp_proj idp,b.abbr abbr,b.title title, a.isfinish isfinish,a.payment pay from sub_projects a '
            'join projects b on a.idp_proj=b.idp where a.idr_proj=%s', (idr,))
        projs = cur.fetchall()
        totalpay = 0
        for p in projs:
            totalpay += p['pay']
        # tests
        cur.execute(
            "select b.test_name name, b.test_desc description, b.priority from sub_tests a join tests b on "
            "a.idt_test=b.idt where a.idr_test=%s order by priority, name", (idr,))
        tests = cur.fetchall()
        # print(params, projs, tests)
        status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
        if request.args.get('notify_delete'):
            status_params['notify_delete'] = request.args.get('notify_delete')
        return render_template('subject_view.html', params=params, records=records, projs=projs, tests=tests,
                               totalpay=totalpay, status_params=status_params)
    else:
        return 'Record not exist'


@bp.route('/view/<idr>/update')
@login_required
def update(idr):
    conn = conn_db()
    cur = conn.cursor(buffered=True, dictionary=True)
    user = g.user
    # current record
    cur.execute('select * from sub_records where binary idu_rec=%s and idr=%s', (user, idr,))
    params = cur.fetchone()
    if params:
        # historic records
        cur.execute("select idr,date_format(record_time,'%Y-%m-%d') as rdate from sub_records where ids_rec=%s "
                    "order by record_time desc", (params['ids_rec'],))
        records = cur.fetchall()
        # projects
        cur.execute(
            'select a.idp_proj idp,b.abbr abbr,b.title title, a.isfinish isfinish,a.payment pay from sub_projects a '
            'join projects b on a.idp_proj=b.idp where a.idr_proj=%s', (idr,))
        projs = cur.fetchall()
        # all projects
        cur.execute("select idp, title, abbr from projects where idu_proj=%s order by record_time DESC", (user,))
        projs_all = cur.fetchall()
        # tests
        # cur.execute(
        #     "select b.test_name name,b.test_desc description, b.priority from sub_tests a join tests b on "
        #     "a.idt_test=b.idt where a.idr_test=%s order by priority ASC", (idr,))
        cur.execute(
            "select idt, test_name name, test_desc description, priority, idt in (select idt_test from sub_tests where "
            "idr_test=%s) ischeck from tests order by priority, name", (idr,))
        tests = cur.fetchall()
        # testlist = list()
        # for test in tests:
        #     testlist.append(test['name'])
        status_params = {'log': 1, 'notindex': 1, 'notregister': 1, 'user': g.user}
        return render_template('subject_update.html', params=params, records=records, projs=projs, projs_all=projs_all,
                               tests=tests, status_params=status_params)
    else:
        return 'Record not exist'


@bp.route('/creating', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        conn = conn_db()
        cur = conn.cursor()
        user = g.user
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
        params = newOrupdate(user, idr, ids, mode='sr')
        # sub ID
        cur.execute('insert into sub_ids values (%s, %s)', (user, ids,))
        # record
        cur.callproc('insert_sub_records', tuple(params.values()))
        # project
        idp_proj = request.form.get('proj_join')
        if idp_proj != 'unknown':
            cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, idp_proj, 'no', 0))
        # test
        idts = request.form.getlist('tests')
        for idt in idts:
            # cur.execute("select idt from tests where test_name=%s", (test,))
            cur.execute("insert into sub_tests values (%s,%s)", (idr, idt))
        conn.commit()
        return idr
    else:
        return 'Error: Data not delivered'
    # return redirect(url_for('projects.new'))


@bp.route('/view/<idr>/modifying', methods=('GET', 'POST'))
@login_required
def modify(idr):
    if request.method == 'POST':
        conn = conn_db()
        cur = conn.cursor()
        user = g.user
        record_date = date.fromisoformat(request.form.get('record_date'))
        is_latest = str(request.form.get('is_latest'))
        # load existing subject ID
        cur.execute("select ids_rec as ids from sub_records where binary idu_rec=%s and idr=%s", (user, idr))
        ids = cur.fetchone()[0]
        if ids:
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
                    cur.execute("select count(*) from sub_records where idr=%s", (idr,))
                    if cur.fetchone()[0] == 0:
                        break
                params = newOrupdate(user, idr, ids, mode='r')  # new record
                # record
                cur.callproc('insert_sub_records', tuple(params.values()))
            else:
                params = newOrupdate(user, idr, ids, mode='n')  # update on existing record
                # record
                # print(params)
                cur.callproc('update_sub_records', tuple(params.values()))
                # print(params)

            # project
            cur.execute("delete from sub_projects where idr_proj=%s", (idr,))
            for proj in projs:
                cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, proj[0], proj[1], proj[2]))
            # test
            idts = request.form.getlist('tests')
            cur.execute("delete from sub_tests where idr_test=%s", (idr,))
            for idt in idts:
                # cur.execute("select idt from tests where test_name=%s", (test,))
                cur.execute("insert into sub_tests values (%s,%s)", (idr, idt))
            conn.commit()
            return idr
        else:
            return 'Error: Record not existing'
    else:
        return 'Error: Data not delivered'


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'GET':
        idr = request.args.get('idr')
        conn = conn_db()
        # cur = conn.cursor()
        cur = conn.cursor(buffered=True, dictionary=True)
        user = g.user
        cur.execute(
            "select ids_rec, date_format(record_time,'%Y-%m-%d') as rdate from sub_records where binary idu_rec=%s and idr=%s",
            (user, idr))
        params = cur.fetchone()
        if params:
            cur.execute('delete from sub_records where binary idu_rec=%s and idr=%s', (user, idr))
            if cur.rowcount == 1:
                conn.commit()
                # remaining records
                cur.execute(
                    "select idr,date_format(record_time,'%Y-%m-%d') as rdate from sub_records where ids_rec=%s order by record_time desc",
                    (params['ids_rec'],))
                records = cur.fetchone()
                if records:
                    return redirect(url_for('subject.view_single', idr=records['idr'], notify_delete=params['rdate']))
                else:
                    cur.execute('delete from sub_ids where binary idu_rec=%s and ids=%s', (user, params['ids_rec']))
                    conn.commit()
                    return 'Successfully delete'
            else:
                return 'Failed! More than on record affected'
        else:
            return 'Record not exist'


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
        for i in range(len(fo)):
            fo[i] = fo[i] if fo[i] > -20 else None
            thresh.append(fo[i])
        try:
            #     freqs = ['125', '250', '500', '750', '1000', '1500', '2000', '3000', '4000', '6000', '8000']
            ave = sum(fo[2:9:2]) / 4
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


def newOrupdate(user, idr, ids, mode='n'):
    # add new record id
    params = dict()
    cur_time = datetime.now()
    params['idu_rec'] = user
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

    freqs = ['125', '250', '500', '750', '1000', '1500', '2000', '3000', '4000', '6000', '8000']
    airR = [request.form.get('air_' + f + 'r') for f in freqs]
    airL = [request.form.get('air_' + f + 'l') for f in freqs]
    boneR = [request.form.get('bone_' + f + 'r') for f in freqs]
    boneL = [request.form.get('bone_' + f + 'l') for f in freqs]
    params['air_125r'], params['air_250r'], params['air_500r'], params['air_750r'], params['air_1000r'], params[
        'air_1500r'], params['air_2000r'], params['air_3000r'], params['air_4000r'], params['air_6000r'], params[
        'air_8000r'], params['air_avgr'], params['air_levelr'], params['air_125l'], params['air_250l'], params[
        'air_500l'], params['air_750l'], params['air_1000l'], params[
        'air_1500l'], params['air_2000l'], params['air_3000l'], params['air_4000l'], params['air_6000l'], params[
        'air_8000l'], params['air_avgl'], params['air_levell'], params['bone_125r'], params['bone_250r'], params[
        'bone_500r'], params['bone_750r'], params['bone_1000r'], params['bone_1500r'], params['bone_2000r'], params[
        'bone_3000r'], params['bone_4000r'], params[
        'bone_6000r'], params['bone_8000r'], params['bone_avgr'], params['bone_levelr'], params['bone_125l'], params[
        'bone_250l'], params['bone_500l'], params['bone_750l'], params['bone_1000l'], params['bone_1500l'], params[
        'bone_2000l'], params[
        'bone_3000l'], params['bone_4000l'], params['bone_6000l'], params['bone_8000l'], params['bone_avgl'], params[
        'bone_levell'] = cal_thresh((airR, airL, boneR, boneL))
    params['cause_right'] = request.form.get('cause_right')
    params['cause_left'] = request.form.get('cause_left')
    params['shape_right'] = request.form.get('shape_right')
    params['shape_left'] = request.form.get('shape_left')
    params['immittance_right'] = request.form.get('immittance_right')
    params['immittance_left'] = request.form.get('immittance_left')
    params['speech'] = request.form.get('speech')
    return params
