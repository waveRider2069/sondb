import mysql.connector as sqlconnector
from datetime import datetime
import binascii, os
import xlrd
import re

def create_invcode():
    conn = sqlconnector.connect(user='shaun', password='amituofo8945', database='ssdb',
                                sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION')
    cur = conn.cursor()
    legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    from numpy.random import randint
    try:
        for i in range(20):
            temp = ''
            randi = randint(0, len(legal), 12)
            for j in randi:
                temp += legal[j]
            temp = 'E' + temp
            cur.execute("select idc from codes where idc=%s", (temp,))
            if cur.fetchone() is None:
                cur.execute("insert into codes (idc, maxn,countn) values (%s,1,0)", (temp,))
                print(temp)
        conn.commit()
    except:
        print('error')
        conn.close()
    conn.close()


def import_subjects_Sherry():
    conn = sqlconnector.connect(user='shaun', password='amituofo8945', database='ssdb')
    cur = conn.cursor()
    # cur.execute("delete from sub_records where not exists(select idr_proj from sub_projects where sub_records.idr = sub_projects.idr_proj)")
    # cur.execute("delete from sub_ids where not exists(select ids_rec from sub_records where sub_ids.ids = sub_records.ids_rec)")
    # conn.commit()
    user = 'SonovaRD'
    file = xlrd.open_workbook(r'/Users/shaun/Downloads/Recruiting Projects Registration.xls')
    sheet = file.sheet_by_name('outward')
    labels = ['idcode', 'subname', 'gender', 'age', 'contact', 'update', 'abnormal', 'comments', 'experience',
              'air_250r', 'air_500r', 'air_1000r', 'air_2000r', 'air_4000r', 'air_8000r', 'air_250l', 'air_500l',
              'air_1000l', 'air_2000l', 'air_4000l', 'air_8000l']
    for n in range(1, sheet.nrows):
        values = sheet.row_values(n, 0, 21)
        types = sheet.row_types(n, 0, 21)
        # 1 for text, 2 for float, 3 for empty
        row = dict(zip(labels, values))
        row_type = dict(zip(labels, types))
        # add new subject id
        while True:
            ids = 'S' + binascii.hexlify(os.urandom(7)).decode()
            cur.execute("select count(*) from sub_ids where ids=%s", (ids,))
            if cur.fetchone()[0] == 0:
                break
        while True:
            idr = 'R' + binascii.hexlify(os.urandom(7)).decode()
            cur.execute("select count(*) from sub_records where idr=%s", (idr,))
            if cur.fetchone()[0] == 0:
                break
        params = new_Or_update(user, idr, ids, row, row_type, mode='sr')
        # sub ID
        cur.execute('insert into sub_ids values (%s, %s)', (user, ids,))
        # record
        # print(params)
        cur.callproc('insert_sub_records', tuple(params.values()))
        cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, 'P0b3b1e2c95b4', 'no', 0))
        conn.commit()

        def new_Or_update(user_inner, idr_inner, ids_inner, row_inner, row_type_inner, mode='n'):
            # add new record id
            params_in = dict()
            cur_time = datetime.now()
            params_in['idu_rec'] = user_inner
            params_in['idr'] = idr_inner
            if mode == 'sr' or mode == 'r':
                params_in['ids_rec'] = ids_inner
                params_in['record_time'] = cur_time
            params_in['update_time'] = cur_time
            params_in['subname'] = row_inner.get('subname').strip()
            # row_type: 0 for empty; 1 for str; 2 for num; 3 for date
            if row_type_inner['age'] == 2:
                age = int(row_inner.get('age'))
            else:
                age = None
            params_in['age_record'] = age
            params_in['age'] = age

            if row_type_inner['contact'] == 2:
                phone = str(int(row_inner.get('contact')))
            elif row_type_inner['contact'] == 0:
                phone = None
            else:
                phone = row_inner.get('contact')
            params_in['phone'] = phone

            if row_type_inner['gender'] == 1:
                params_in['gender'] = row_inner.get('gender').strip()
            else:
                params_in['gender'] = None
            params_in['attitude'] = None
            params_in['location'] = None
            params_in['spare'] = None
            params_in['sparenote'] = None
            params_in['aidwearing'] = None
            if row_type_inner['experience'] == 1:
                exper = row_inner.get('experience').strip()
                if exper.lower() in ['yes', 'experience', 'first', 'first time']:
                    params_in['aidwearing'] = 'either'
            params_in['diseases'] = None
            if row_type_inner['update'] == 3:
                datestr = '更新时间' + xlrd.xldate_as_datetime(row_inner.get('update'), 0).strftime('%Y-%m-%d')
            else:
                datestr = ''
            params_in['comments'] = datestr + row_inner.get('comments').strip()

            airR = [row_inner.get('air_250r'), row_inner.get('air_500r'), row_inner.get('air_1000r'),
                    row_inner.get('air_2000r'), row_inner.get('air_4000r'), row_inner.get('air_8000r')]
            airL = [row_inner.get('air_250l'), row_inner.get('air_500l'), row_inner.get('air_1000l'),
                    row_inner.get('air_2000l'), row_inner.get('air_4000l'), row_inner.get('air_8000l')]
            boneR = [row_inner.get('bone_250r'), row_inner.get('bone_500r'), row_inner.get('bone_1000r'),
                     row_inner.get('bone_2000r'), row_inner.get('bone_4000r'), row_inner.get('bone_8000r')]
            boneL = [row_inner.get('bone_250l'), row_inner.get('bone_500l'), row_inner.get('bone_1000l'),
                     row_inner.get('bone_2000l'), row_inner.get('bone_4000l'), row_inner.get('bone_8000l')]

            params_in['air_250r'], params_in['air_500r'], params_in['air_1000r'], params_in['air_2000r'], params_in['air_4000r'], \
            params_in[
                'air_8000r'], params_in['air_avgr'], params_in['air_levelr'], params_in['air_250l'], params_in['air_500l'], params_in[
                'air_1000l'], params_in['air_2000l'], params_in['air_4000l'], params_in['air_8000l'], params_in['air_avgl'], params_in[
                'air_levell'], params_in['bone_250r'], params_in['bone_500r'], params_in['bone_1000r'], params_in['bone_2000r'], \
            params_in[
                'bone_4000r'], params_in['bone_8000r'], params_in['bone_avgr'], params_in['bone_levelr'], params_in['bone_250l'], \
            params_in['bone_500l'], params_in['bone_1000l'], params_in['bone_2000l'], params_in['bone_4000l'], params_in['bone_8000l'], \
            params_in['bone_avgl'], params_in['bone_levell'] = cal_thresh((airR, airL, boneR, boneL))

            params_in['cause_right'] = None
            params_in['cause_left'] = None
            params_in['shape_right'] = None
            params_in['shape_left'] = None
            params_in['immittance_right'] = None
            params_in['immittance_left'] = None
            params_in['speech'] = None
            return params_in


def import_subjects_LiMingS():

    def new_or_update(user_inner, idr_inner, ids_inner, row_inner, row_type_inner, mode='n'):
        # add new record id
        params_in = dict()
        cur_time = datetime.now()
        params_in['idu_rec'] = user_inner
        params_in['idr'] = idr_inner
        if mode == 'sr' or mode == 'r':
            params_in['ids_rec'] = ids_inner
            params_in['record_time'] = cur_time
        params_in['update_time'] = cur_time
        params_in['subname'] = row_inner.get('subname').strip()
        # row_type: 0 for empty; 1 for str; 2 for num; 3 for date
        if row_type_inner['age'] == 2:
            age = int(row_inner.get('age'))
        else:
            age = None
        params_in['age_record'] = age
        params_in['age'] = age

        if row_type_inner['contact'] == 2:
            phone = str(int(row_inner.get('contact')))
        elif row_type_inner['contact'] == 0:
            phone = None
        else:
            phone = row_inner.get('contact')
        params_in['phone'] = phone

        if row_type_inner['gender'] == 1:
            params_in['gender'] = row_inner.get('gender').strip()
        else:
            params_in['gender'] = None
        params_in['attitude'] = None
        params_in['location'] = None
        params_in['spare'] = None
        params_in['sparenote'] = None
        # Hearing aid
        HAnum = 0
        HAdescrp = ''
        if row_inner['HAr'].strip():
            HAnum += 1
            HAdescrp += 'HA(R): ' + row_inner['HAr'].strip() + ' / ' + row_inner['Tipr'].strip() + '; '
        if row_inner['HAl'].strip():
            HAnum += 1
            HAdescrp += 'HA(L): ' + row_inner['HAl'].strip() + ' / ' + row_inner['Tipl'].strip() + '; '

        params_in['aidwearing'] = [None, 'unilateral', 'bilateral'][HAnum]
        params_in['diseases'] = None
        # comments
        params_in['comments'] = HAdescrp if HAdescrp else None
        freqs = ['125', '250', '500', '750', '1000', '1500', '2000', '3000', '4000', '6000', '8000']
        airR = [row_inner.get('air_' + f + 'r') for f in freqs]
        airL = [row_inner.get('air_' + f + 'l') for f in freqs]
        boneR = [row_inner.get('bone_' + f + 'r') for f in freqs]
        boneL = [row_inner.get('bone_' + f + 'l') for f in freqs]

        params_in['air_125r'], params_in['air_250r'], params_in['air_500r'], params_in['air_750r'], params_in['air_1000r'], params_in[
            'air_1500r'], params_in['air_2000r'], params_in['air_3000r'], params_in['air_4000r'], params_in['air_6000r'], \
        params_in[
            'air_8000r'], params_in['air_avgr'], params_in['air_levelr'], params_in['air_125l'], params_in['air_250l'], params_in[
            'air_500l'], params_in['air_750l'], params_in['air_1000l'], params_in[
            'air_1500l'], params_in['air_2000l'], params_in['air_3000l'], params_in['air_4000l'], params_in['air_6000l'], \
        params_in[
            'air_8000l'], params_in['air_avgl'], params_in['air_levell'], params_in['bone_125r'], params_in['bone_250r'], \
        params_in[
            'bone_500r'], params_in['bone_750r'], params_in['bone_1000r'], params_in['bone_1500r'], params_in['bone_2000r'], \
        params_in[
            'bone_3000r'], params_in['bone_4000r'], params_in[
            'bone_6000r'], params_in['bone_8000r'], params_in['bone_avgr'], params_in['bone_levelr'], params_in['bone_125l'], \
        params_in[
            'bone_250l'], params_in['bone_500l'], params_in['bone_750l'], params_in['bone_1000l'], params_in['bone_1500l'], \
        params_in[
            'bone_2000l'], params_in[
            'bone_3000l'], params_in['bone_4000l'], params_in['bone_6000l'], params_in['bone_8000l'], params_in['bone_avgl'], \
        params_in[
            'bone_levell'] = cal_thresh((airR, airL, boneR, boneL))

        params_in['cause_right'] = None
        params_in['cause_left'] = None
        params_in['shape_right'] = None
        params_in['shape_left'] = None
        params_in['immittance_right'] = None
        params_in['immittance_left'] = None
        params_in['speech'] = None
        return params_in

    conn = sqlconnector.connect(user='shaun', password='amituofo8945', database='ssdb')
    cur = conn.cursor()
    # cur.execute("delete from sub_ids Where ids in (SELECT ids_rec FROM sub_records WHERE idr in (SELECT idr_proj FROM sub_projects WHERE idp_proj='P63f438360b94'))")
    # conn.commit()
    user = 'SonovaRD'
    file = xlrd.open_workbook(r'/Users/shaun/Documents/Database/subject_database_0805.xlsx')
    sheet = file.sheet_by_name('internalSimple')
    labels = ['subname', 'gender', 'age', 'address', 'contact',
              'air_125r','air_250r', 'air_500r','air_750r', 'air_1000r','air_1500r','air_2000r','air_3000r','air_4000r','air_6000r', 'air_8000r',
              'air_125l', 'air_250l', 'air_500l', 'air_750l', 'air_1000l', 'air_1500l', 'air_2000l', 'air_3000l',
              'air_4000l', 'air_6000l', 'air_8000l',
              'bone_125r', 'bone_250r', 'bone_500r', 'bone_750r', 'bone_1000r', 'bone_1500r', 'bone_2000r', 'bone_3000r',
              'bone_4000r', 'bone_6000r', 'bone_8000r',
              'bone_125l', 'bone_250l', 'bone_500l', 'bone_750l', 'bone_1000l', 'bone_1500l', 'bone_2000l', 'bone_3000l',
              'bone_4000l', 'bone_6000l', 'bone_8000l','HAr','Tipr','HAl','Tipl']

    for n in range(2, sheet.nrows):
        values = sheet.row_values(n, 1, 56)
        types = sheet.row_types(n, 1, 56)
        # 1 for text, 2 for float, 3 for empty
        row = dict(zip(labels, values))
        row_type = dict(zip(labels, types))
        # add new subject id
        while True:
            ids = 'S' + binascii.hexlify(os.urandom(7)).decode()
            cur.execute("select count(*) from sub_ids where ids=%s", (ids,))
            if cur.fetchone()[0] == 0:
                break
        while True:
            idr = 'R' + binascii.hexlify(os.urandom(7)).decode()
            cur.execute("select count(*) from sub_records where idr=%s", (idr,))
            if cur.fetchone()[0] == 0:
                break
        params_in = new_or_update(user, idr, ids, row, row_type, mode='sr')
        # sub ID
        cur.execute('insert into sub_ids values (%s, %s)', (user, ids,))
        # record
        # print(params)
        cur.callproc('insert_sub_records', tuple(params_in.values()))
        cur.execute("insert into sub_projects values (%s,%s,%s,%s)", (idr, 'P63f438360b94', 'no', 0))
        conn.commit()

        def new_Or_update(user_inner, idr_inner, ids_inner, row_inner, row_type_inner, mode='n'):
            # add new record id
            params_in = dict()
            cur_time = datetime.now()
            params_in['idu_rec'] = user_inner
            params_in['idr'] = idr_inner
            if mode == 'sr' or mode == 'r':
                params_in['ids_rec'] = ids_inner
                params_in['record_time'] = cur_time
            params_in['update_time'] = cur_time
            params_in['subname'] = row_inner.get('subname').strip()
            # row_type: 0 for empty; 1 for str; 2 for num; 3 for date
            if row_type_inner['age'] == 2:
                age = int(row_inner.get('age'))
            else:
                age = None
            params_in['age_record'] = age
            params_in['age'] = age

            if row_type_inner['contact'] == 2:
                phone = str(int(row_inner.get('contact')))
            elif row_type_inner['contact'] == 0:
                phone = None
            else:
                phone = row_inner.get('contact')
            params_in['phone'] = phone

            if row_type_inner['gender'] == 1:
                params_in['gender'] = row_inner.get('gender').strip()
            else:
                params_in['gender'] = None
            params_in['attitude'] = None
            params_in['location'] = None
            params_in['spare'] = None
            params_in['sparenote'] = None
            #Hearing aid
            HAnum = 0
            HAdescrp = ''
            if row_inner['HAr'].strip():
                HAnum += 1
                HAdescrp += 'HA(R): ' + row_inner['HAr'].strip() + ' / ' + row_inner['Tipr'].strip() + '; '
            if row_inner['HAl'].strip():
                HAnum += 1
                HAdescrp += 'HA(L): ' + row_inner['HAl'].strip() + ' / ' + row_inner['Tipl'].strip() + '; '

            params_in['aidwearing'] = [None, 'unilateral', 'bilateral'][HAnum]
            params_in['diseases'] = None
            # comments
            params_in['comments'] = HAdescrp if HAdescrp else None
            freqs = ['125', '250', '500', '750', '1000', '1500', '2000', '3000', '4000', '6000', '8000']
            airR = [row_inner.get('air_' + f + 'r') for f in freqs]
            airL = [row_inner.get('air_' + f + 'l') for f in freqs]
            boneR = [row_inner.get('bone_' + f + 'r') for f in freqs]
            boneL = [row_inner.get('bone_' + f + 'l') for f in freqs]

            params_in['air_125r'], params_in['air_250r'], params_in['air_500r'], params_in['air_750r'], params_in['air_1000r'], params_in[
                'air_1500r'], params_in['air_2000r'], params_in['air_3000r'], params_in['air_4000r'], params_in['air_6000r'], \
            params_in[
                'air_8000r'], params_in['air_avgr'], params_in['air_levelr'], params_in['air_125l'], params_in['air_250l'], params_in[
                'air_500l'], params_in['air_750l'], params_in['air_1000l'], params_in[
                'air_1500l'], params_in['air_2000l'], params_in['air_3000l'], params_in['air_4000l'], params_in['air_6000l'], \
            params_in[
                'air_8000l'], params_in['air_avgl'], params_in['air_levell'], params_in['bone_125r'], params_in['bone_250r'], \
            params_in[
                'bone_500r'], params_in['bone_750r'], params_in['bone_1000r'], params_in['bone_1500r'], params_in['bone_2000r'], \
            params_in[
                'bone_3000r'], params_in['bone_4000r'], params_in[
                'bone_6000r'], params_in['bone_8000r'], params_in['bone_avgr'], params_in['bone_levelr'], params_in['bone_125l'], \
            params_in[
                'bone_250l'], params_in['bone_500l'], params_in['bone_750l'], params_in['bone_1000l'], params_in['bone_1500l'], \
            params_in[
                'bone_2000l'], params_in[
                'bone_3000l'], params_in['bone_4000l'], params_in['bone_6000l'], params_in['bone_8000l'], params_in['bone_avgl'], \
            params_in[
                'bone_levell'] = cal_thresh((airR, airL, boneR, boneL))

            params_in['cause_right'] = None
            params_in['cause_left'] = None
            params_in['shape_right'] = None
            params_in['shape_left'] = None
            params_in['immittance_right'] = None
            params_in['immittance_left'] = None
            params_in['speech'] = None
            return params_in


def cal_thresh(form):
    thresh = list()
    for fo in form:
        # fo = list(map(int, fo))
        for i in range(len(fo)):
            foi = fo[i]
            try:
                foi = round5(int(foi))
                if foi <= -20:
                    foi = None
            except:
                if isinstance(foi, str):
                    ds = re.match('\d+', foi)
                    if ds:
                        foi = round5(int(ds.group(0)))
                    else:
                        foi = None
                else:
                    foi = None
            fo[i] = foi
            thresh.append(fo[i])
        try:
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


def round5(val):
    val = round(val)
    s = int(str(val)[-1])
    if s < 3:
        return val - int(s*val/abs(val))
    elif s < 8:
        return val + int((5 - s)*val/abs(val))
    else:
        return val + int((10 - s)*val/abs(val))

