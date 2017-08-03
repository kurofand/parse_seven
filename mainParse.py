# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time

def getHTML(url):
	html=requests.get(url)
	data=html.text
	body=BeautifulSoup(data, 'lxml')
	return(body)

body=getHTML('https://www.navitime.co.jp/category/0201001001')
selectPref=body.find('select', {'id':'prefecture_select'})
prefList=selectPref.findChildren('option')
recordCount=0
startTime=datetime.now()
for prefecture in prefList:
	if(prefecture['value']!=""):
		file=open('txt_files/'+prefecture.text+'.txt', 'w')
		#this request return a json obj with cities id which will be used for switch pages
		html=requests.get('https://www.navitime.co.jp/async/category/addressList?addressCode=%s'%prefecture['value'])
		js=json.loads(html.text)
		for code in js:
			page=1
			while True:
				body=getHTML('https://www.navitime.co.jp/category/0201001001/%s?page=%s'%(code['code'], page))
				linkDiv=body.find('div', {'id':'spot_list'})
				linkDl=linkDiv.findChildren('dl', {'class':'list_item_frame'})
				#if it was found there is page with page number, else out of page list, end loop
				if(linkDl):
					page=page+1
					for dl in linkDl:
						link=dl.find('a')
						name=link.text
						addr=dl.find('dd').contents[0]
						file.write('%s\n%s\n'%(name.encode('utf-8'), addr.encode('utf-8')))
						recordCount=recordCount+1
				else:
					break
			print('%s has done'%code['name'])
		
		file.close()
		print('%s has done'%prefecture.text)
		time.sleep(120)	
print('All done, %s records writed'%recordCount)
endTime=datetime.now()
print('It taked %s'%str(endTime-startTime))
