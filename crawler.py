import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url, encode = 'utf-8'):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = encode
		return r.text
	except:
		return ""  

def getCityList(list, name_list, cityURL):
	html = getHTMLText(cityURL)
	soup = BeautifulSoup(html, 'html.parser')
	a = soup.find_all("a", class_ = "NtnlSummaryCity")
	for i in a:
		try:
			href = i.attrs['href']
			list.append(re.search(r'\d{3}', href))
			name_list.append(i.string)
		except:
			continue

def getCCDetails(CC_detail, CClist):
	AQI_table = CC_detail.find('table')

	line = []
	observed = AQI_table.find('small').string
	line.append(observed)

	for i in AQI_table.find('table').find('table').children:
		if i != '\n':
			for j in i.children:
				if j != '\n':
					CAQI = "AQI="+j.string.strip()
	line.append(CAQI)

	CAQI_level = AQI_table.find(class_='AQDataLg').string
	line.append(CAQI_level)
	line = ', '.join(line)

	pollutant_detail=[]
	for i in AQI_table.next_siblings:
		if i.find('table') != None and str(i.find('table')) != '-1':
			table = i.find('table')
			for tr in table.children:
				if tr != '\n':
					dt_list=[]
					for td in tr.find_all('td'):
						if td.string != None:
							dt_list.append(td.string.strip())
					dt_list.append(tr.find('a').string.strip())
					pollutant_detail.append(', '.join(dt_list))
	line = line+ '; ' + '; '.join(pollutant_detail)
	CClist.append(line)

def getCCInfo(CC_detail, CClist):
	if CC_detail.string == None:
		CClist.append('| Current conditions: ')
		getCCDetails(CC_detail, CClist)
	else:
		CClist.append('| Current conditions: n/a')

def getFAQIDetails(td, forcast_list):
	line = []

	AQI_level = td.find(class_='AQILegendText').string.strip()
	if td.find('table', class_='TblInvisible') == None:
		line = 'AQI level = '+AQI_level+';'
	else:
		for i in td.find('table', class_='TblInvisible').children:
			if i != '\n':
				for j in i.children:
					if j != '\n':
						AQI = "AQI = "+j.string.strip()
		line.append(AQI)
		line.append(AQI_level+';')
		line = ', '.join(line)
	forcast_list.append(line)

def getForecastAQI(td, forcast_list, str):
	if td.string == None:
		forcast_list.append('| Forcast - '+str+': ')
		getFAQIDetails(td, forcast_list)
	else:
		forcast_list.append('| Forcast - '+str+': n/a')

def getFPDDetails(td, forcast_list):
	line = []
	pair = []
	for i in td.find_all(class_='AQDataPollDetails'):
		if i.string != None:
			par = i.string.strip()
			pair.append(par)
			j = i.next_sibling.next_sibling.find('table').find(height = '27')
			if j != None:
				num = j.string.strip()
				pair.append('='+num)
		# possiblly need: and str(i.find('table')) != '-1'
		elif i.find('a') != None:
			msg = i.find('a').string.strip()
			pair.append('('+msg+')')
			pair=''.join(pair)
			line.append(pair)
			pair = []
		else:
			pair=''.join(pair)
			line.append(pair)
			pair = []

	line = ', '.join(line)
	forcast_list.append(line)

def getForecastPD(td, forcast_list):
	if td.string == None:
		forcast_list.append('Pollutant Details : ')
		getFPDDetails(td, forcast_list)
	else:
		forcast_list.append('Pollutant Details : n/a')

def getAQInfo(html, city_info, info_list):
	soup = BeautifulSoup(html, 'html.parser')

	# Get city name
	city_name = soup.find(class_='ActiveCity').string.strip()
	city_info.append(city_name)
	
	# Get current conditions
	current_table = soup.find(title = 'Current Conditions').parent.parent
	detail = current_table.find(class_='AQDataSectionTitle')
	getCCInfo(detail, city_info)

	# Get Forecast information
	forecast_table = current_table.next_sibling.next_sibling
	
	today_AQI_td = forecast_table.find(class_='AQDataContent')
	getForecastAQI(today_AQI_td, city_info, 'Today')

	test = forecast_table.find_all(class_='AQDataContent')
	count = 1
	for td in test:
		if count == 3:
			today_PD_td = td
			break
		count += 1	
	getForecastPD(today_PD_td, city_info)

	count = 1
	for td in test:
		if count == 2:
			tmr_AQI_td = td
			break
		count+=1
	getForecastAQI(tmr_AQI_td, city_info, 'Tomorrow')

	count = 1
	for td in test:
		if count == 4:
			tmr_PD_td = td
			break
		count += 1
	getForecastPD(tmr_PD_td, city_info)

	# Concatenate
	city_info = ' '.join(city_info)
	info_list.append(city_info)

def getAllAQInfo(list, cityURL, info_list):
	for city in list:
		url = cityURL + city.group(0)
		html = getHTMLText(url)
		city_info = []
		try:
			if html == "":
				continue
			getAQInfo(html, city_info, info_list)
		except:
			traceback.print_exc()
			continue

def getSingleAQInfo(cityURL, info_list):
	html = getHTMLText(cityURL)
	city_info = []
	getAQInfo(html, city_info, info_list)
	# return city_info

def getInfoGivenInput(given_input):
	"""
	Get specified city's air quality information
	"""
	city_list_url = 'https://airnow.gov/index.cfm?action=airnow.local_state&stateid=5'
	aq_info_url = 'https://airnow.gov/index.cfm?action=airnow.local_city&mapcenter=0&cityid='
	city_list = []
	city_name_list = []
	getCityList(city_list, city_name_list, city_list_url)
	ind = city_name_list.index(given_input)
	aq_info_url = aq_info_url + city_list[ind].group(0)
	info = []
	getSingleAQInfo(aq_info_url, info)
	return info[0]

def getInfo():
	"""
	Get all city's air quality information in California
	"""
	city_list_url = 'https://airnow.gov/index.cfm?action=airnow.local_state&stateid=5'
	aq_info_url = 'https://airnow.gov/index.cfm?action=airnow.local_city&mapcenter=0&cityid='
	city_list = []
	city_name_list = []
	getCityList(city_list, city_name_list, city_list_url)
	info = []
	getAllAQInfo(city_list, aq_info_url, info)
	
	# for i in info:
	# 	print(i)
	return info

if __name__ == '__main__':
	print(getInfo())
	print(getInfoGivenInput("Bishop")) # Take Bishop as an example