# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

def getHTML(url):
	html=requests.get(url)
	data=html.text
	body=BeautifulSoup(data, 'lxml')
	return(body)

body=getHTML('https://www.navitime.co.jp/category/0201001001')
selectPref=body.find('select', {'id':'prefecture_select'})
prefList=selectPref.findChildren('option')
for prefecture in prefList:
	if(prefecture['value']=="01"):
		#this request return a json obj with cities id which will be used for switch pages
		html=requests.get('https://www.navitime.co.jp/async/category/addressList?addressCode=%s'%prefecture['value'])
		js=json.loads(html.text)
		for code in js:
			if(code['code']=='01101'):
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
							#operators under comment needs for get work time and avalible service but not all shops has it
							#if it will be neccessary I will make a some check but now only take a name and address of shop
							#from front page
							#body=getHTML('https:'+link['href'])
							#detailDiv=body.find('div', {'class':'detail_contents'})
							#detailDD=detailDiv.findChildren('dd')
							#address=detailDD[0].string
							#work_time=detailDD[3].string
							#service=detailDD[4].text
							#print(work_time)
							name=link.text
							addr=dl.find('dd').contents[0]
							
							
					else:
						break
				
		#print(body)
		#selectCity=body.find('select', {'id':'city_select'})
		#cityList=selectCity.findChildren('option')
		#for city in cityList:
		#	if(city['value']!=""):
		#		print(city.text)
