import datetime
ta = str(datetime.datetime.now())
print(ta[0:19])
print(type(ta))

now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d")
print(otherStyleTime)
print(type(otherStyleTime))