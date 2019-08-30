import datetime


def time_ration(ta, tb):
    sec1 = datetime.timedelta(seconds=1)
    ta_format = datetime.datetime.fromisoformat('2019-06-01 ' + ta)
    tb_format = datetime.datetime.fromisoformat('2019-06-01 ' + tb)
    while ta_format <= tb_format:
        cur_time = ta_format
        time_str = isrational(cur_time)
        if time_str:
            print(time_str)
        ta_format = ta_format + sec1


def isrational(cur_time):
    time_str = cur_time.strftime('%H:%M:%S')
    for s in time_str:
        if s in '34679':
            return False
    time_dic = zip(['hour', 'min', 'sec'], time_str.split(':'))
    for la, val in time_dic:
        v1 = val[0]
        v2 = val[1]
        if v1 in '25':
            v1 = '2' if v1 == '5' else '5'
        if v2 in '25':
            v2 = '2' if v2 == '5' else '5'
        val = v2 + v1
        if (la == 'hour' or la == 'min') and int(val) > 60:
            return False
        elif la == 'sec' and int(val) > 24:
            return False
    return time_str


if __name__ == '__main__':
    time_ration('00:00:01', '01:20:40')
