import requests
from datetime import datetime
import pytz

#r=requests.get('https://api.github.com/users/GurpreetS2001')
#print(r.json())
#print(r.json()['followers'])
#print("----------------------")
#r2=requests.get('https://api.github.com/users/GurpreetS2001/repos')
#print(r2.json())
#time=r.json()['updated_at']
#print(datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'))
#print(datetime.datetime(2015, 10, 9, 23, 55, 59))
print(datetime.now(pytz.timezone('Asia/Kolkata')))
print(datetime.now())
x=datetime.now().astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None)
print(x)
