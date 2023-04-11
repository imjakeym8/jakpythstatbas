from datetime import datetime, timezone, timedelta

UTC = timezone.utc # Output: UTC
UTC8 = timezone(timedelta(hours=8)) #Output: UTC+08:00
UTC9 = timezone(timedelta(hours=9)) #Output: UTC+09:00

t = datetime.today() #returns your system local datetime
tn = datetime.now() #returns your system local datetime with an option to pass in a timezone parameter using 'tz=', making it time-zone aware.
tun = datetime.utcnow() #returns your system local datetime converted to UTC with an option to add a timezone parameter using '.replace(tzinfo=)', making it time-zone aware.
now_utc = tun.replace(tzinfo=UTC) #using .replace() method to add a timezone value, making it time-zone aware.
tnz = datetime.now(UTC9) #more efficient way of converting timezones

print(t)
print(tn)
print(tun)
print(UTC)
print(UTC8)
print(now_utc)
print(tnz)

formatted_time = now_utc.strftime('%A, %B %d, %Y %I:%M:%S %z %Z') #formats the datetime object into any way you desire, given the proper format codes: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
print((formatted_time))
str_time = datetime.strptime(formatted_time,'%A, %B %d, %Y %I:%M:%S %z %Z') #parses the datetime string to an datetime object
print(str_time)