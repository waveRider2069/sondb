from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
# from werkzeug.exceptions import abort

from .auth import login_required
from .db import conn_db

bp = Blueprint('consult', __name__, url_prefix='/consult')


@bp.route('/')
@login_required
def ready():
    return render_template('consult_1.html')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    params = get_params()
    try:
        params['page'] = abs(int(request.args.get('page')))
    except:
        params['page'] = 1
    # 20 box per page
    boxes = 20
    conn = conn_db()
    cur = conn.cursor()
    # if tests tage
    if params['tests']:
        # cur.execute(f"create temporary table t_tags (select * from (select idr from tests_tag where "
        #             f"find_in_set(tname, '{','.join(params['tests'])}')>0) raw group by idr having "
        #             f"count(*)={len(params['tests'])})")
        cur.execute(f"create temporary table t_tags (select idr from tests_tag where "
                    f"find_in_set(tname, '{','.join(params['tests'])}')>0)")
    else:
        cur.execute("create temporary table t_tags (select 'all')")
    # sort
    sort = request.args.get('sort')
    if sort and sort in ['2', '3', '4']:
        params['sort'] = sort
    else:
        params['sort'] = '1'
    # call search procedure
    cur.callproc('search_subs', (
        params['sort'], params['key_str'], params['level'], params['cause'], params['shape'], params['symmetry'],
        params['speech'],
        params['gender'], params['attitude'], params['location'], params['spare'], params['teststr'], params['ageDw'],
        params['ageUp'], params['f250aUp'], params['f500aUp'], params['f1000aUp'], params['f2000aUp'],
        params['f4000aUp'],
        params['f8000aUp'], params['f250bUp'], params['f500bUp'], params['f1000bUp'], params['f2000bUp'],
        params['f4000bUp'], params['f8000bUp'], params['f250aDw'], params['f500aDw'], params['f1000aDw'],
        params['f2000aDw'], params['f4000aDw'], params['f8000aDw'], params['f250bDw'], params['f500bDw'],
        params['f1000bDw'], params['f2000bDw'], params['f4000bDw'], params['f8000bDw']))
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
        cur.execute("select idp, abbr from projects")
        projs = cur.fetchall()
    cur.execute("drop table if exists t_tags")
    cur.execute("drop table if exists subs_search")
    return render_template('consult_res.html', reclist=curlist, params=params, projs=projs)


@bp.route('/switch')
@login_required
def switch_date():
    pass


def get_params():
    params = dict()
    # Form field folded up or unfolded
    params['hearf'] = request.args.get('hearf')
    params['personf'] = request.args.get('personf')
    params['experf'] = request.args.get('experf')
    # conditions
    params['level'] = ','.join(request.args.getlist('level'))
    params['cause'] = ','.join(request.args.getlist('cause'))
    params['shape'] = ','.join(request.args.getlist('shape'))
    params['symmetry'] = ','.join(request.args.getlist('symmetry'))
    params['speech'] = ','.join(request.args.getlist('speech'))
    params['gender_lst'] = request.args.getlist('gender')
    params['gender'] = ','.join(params['gender_lst'])
    params['attitude'] = ','.join(request.args.getlist('attitude'))
    params['location'] = ','.join(request.args.getlist('location'))
    params['spare'] = ','.join(request.args.getlist('spare'))
    params['tests'] = request.args.getlist('tests')
    params['teststr'] = ','.join(params['tests'])
    # age, thresholds
    for item in ['ageDw', 'ageUp', 'f250aUp', 'f500aUp', 'f1000aUp', 'f2000aUp', 'f4000aUp', 'f8000aUp', 'f250bUp',
                 'f500bUp', 'f1000bUp', 'f2000bUp', 'f4000bUp', 'f8000bUp', 'f250aDw', 'f500aDw', 'f1000aDw',
                 'f2000aDw', 'f4000aDw', 'f8000aDw', 'f250bDw',
                 'f500bDw', 'f1000bDw', 'f2000bDw', 'f4000bDw', 'f8000bDw']:
        try:
            params[item] = int(request.args.get(item))
        except TypeError or ValueError:
            params[item] = None
    keylist = request.args.get('keys').strip().split(' ')
    while '' in keylist:
        keylist.remove('')
    # params['keys'] = keylist
    params['key_str'] = ' '.join(keylist)
    # params['key_str'] = request.args.get('keys').strip()
    # print(params['key_str'])
    return params

# "select ids_rec ids, idr, group_concat(idr) idrs, group_concat(subname) subnames from sub_records group by ids_rec order by update_time"
#
# "select sproj.idr_proj idr,group_concat(pp.idp) idp, group_concat(pp.abbr) abbrs from sub_projects sproj join projects pp on pp.idp=sproj.idp_proj group by sproj.idr_proj"


# "select ss.*,proj.abbr from (select srec.*,sproj.idp_proj idp from "
#                 "(select ids_rec ids, idr,group_concat(idr) idrs, subname from sub_records group by ids_rec) srec "
#                 "join sub_projects sproj on srec.idr=sproj.idr_proj group by ) ss join projects proj "
#                 "on proj.idp = ss.idp"


# "select ss.*,proj.abbr from (select srec.*,sproj.idp_proj idp from (select ids_rec ids, idr,group_concat(idr) idrs, subname,age,attitude,gender,location,spare from sub_records group by ids_rec) srec join sub_projects sproj on srec.idr=sproj.idr_proj) ss join projects proj on proj.idp = ss.idp;"
