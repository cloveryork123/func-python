import datetime
import time

yestoday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%d-%m-%y')
print("yestoday:",yestoday)

today = datetime.date.today().strftime('%d-%m-%y')
print("today:",today)
today_0_timestamp = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))
print("today_0_timestamp:",today_0_timestamp)
today_20_timestamp = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) + 20*3600
print("today_20_timestamp:",today_20_timestamp)
current_timestamp = int(time.time())
print("current_timestamp:",current_timestamp)
delay = today_20_timestamp - current_timestamp
print("today20_current delay:", delay, "hour:", delay/3600)
print()

utc_now = datetime.datetime.utcnow()  # 获取当前的UTC时间
print("utc_now:",utc_now)
timestamp = int(utc_now.timestamp())  # 转换为时间戳
print("timestamp:",timestamp)
date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
print("date_str:", date_str)
print()

from datetime import datetime as dt

date_string = "2024-08-29T20:00:00.000Z"
print("date_string:",date_string)
datetime_obj = dt.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
timestamp = datetime_obj.timestamp()
print("timestamp:",timestamp)
date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
print("date_str:", date_str)

timestamp2 = int(dt.fromisoformat(date_string.replace("Z", "+00:00")).timestamp())
print("timestamp2:",timestamp2)
date_string2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp2))
print("date_string2:", date_string2)
