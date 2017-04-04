import requests
import sys
from flaskupload import *

print("start")
url = "http://localhost:5000/"
r = requests.get(url)
print ("GET= " + r.text)
files = {'input_pic': ('pct.jpg', open('pct.jpg', 'rb')), 'input_style': ('style.jpg', open('style.jpg', 'rb'))}
payload = {'num': '8'}
r = requests.post(url + "upload", data=payload, files=files)
print ("POST=" + r.text)
sys.exit()
