import calendar, datetime, time

moon_datetime_a = datetime.datetime(1969, 7, 20, 20, 17, 40)  # year,month,day,hour,minute,second
print(moon_datetime_a)  # 1969-07-20 20:17:40
moon_time = calendar.timegm(moon_datetime_a.utctimetuple())  # returns seconds
print(moon_time)  # -14182940
moon_datetime_b = datetime.datetime.utcfromtimestamp(moon_time)
print(moon_datetime_b)  # 1969-07-20 20:17:40
moon_datetime_a_isoformat = moon_datetime_a.isoformat()
print(moon_datetime_a_isoformat)  # 1969-07-20T20:17:40
moon_datetime_b_isoformat = moon_datetime_b.isoformat()
print(moon_datetime_b_isoformat)  # 1969-07-20T20:17:40
time_strftime = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(moon_time))  # string from time
print(time_strftime)  # 1969-07-20T20:17:40
current_a = datetime.datetime.utcnow()
print(current_a)
current_b = datetime.datetime.now()
print(current_b)