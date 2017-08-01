# -*- coding: utf-8 -*-

import requests
#import json
#from bs4 import BeautifulSoup

url='https://www.navitime.co.jp/category/0201001001/13101/'
html=requests.get(url)
data=html.text
print(data)
