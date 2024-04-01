import requests
from bs4 import BeautifulSoup
import datetime

def gettitle(x):
	url = f'https://scrapethissite.com/pages/forms/?page_num={x}'
	r = requests.get(url)
	sp = BeautifulSoup(r.text, 'html.parser')
	print(sp.title.text)
	return

def gettitle_session(x):
	url = f'https://scrapethissite.com/pages/forms/?page_num={x}'
	r = s.get(url)
	sp = BeautifulSoup(r.text, 'html.parser')
	print(sp.title.text)
	return

# w/o session 0:00:07.904826
# with session 0:00:03.712835
if __name__=='__main__':
	s = requests.Session()
	start = datetime.datetime.now()
	for x in range(1,21):
		#gettitle(x)
		gettitle_session(x)
	finish = datetime.datetime.now() - start
	print(finish)