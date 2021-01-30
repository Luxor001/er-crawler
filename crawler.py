import math
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def decodeURL(pagina, stringa):
	URL = f'http://servizissiir.regione.emilia-romagna.it/deliberegiunta/servlet/AdapterHTTP?MODE_VIEW=AJAX&ACTION_NAME=ACTIONRICERCADELIBERE&ENTE=1&tipoAtto=&annoAdozione=2020&numAdozione=&dataAdozioneDa=&dataAdozioneA=&oggetto={stringa}&did=true&POPULATING=LIST&tableId=ricerca_delibere&_=1611778488297&&ricerca_delibere_LIST_PAGE={pagina}'
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'lxml')
	rows = soup.find_all('row')
	for riga in rows:
		dataRiga = 	datetime.strptime(riga.get('data_adozione_dl'),  '%d/%m/%Y')
		dataCorrente = datetime.today()
		if dataRiga.date() == dataCorrente.date():
			s  = 2
	
paginaCorrente = 1
stringaRicerca = 'so'
URL = f'http://servizissiir.regione.emilia-romagna.it/deliberegiunta/servlet/AdapterHTTP?MODE_VIEW=AJAX&ACTION_NAME=ACTIONRICERCADELIBERE&ENTE=1&tipoAtto=&annoAdozione=2020&numAdozione=&dataAdozioneDa=&dataAdozioneA=&oggetto={stringaRicerca}&did=true&POPULATING=LIST&tableId=ricerca_delibere&_=1611778488297&&ricerca_delibere_LIST_PAGE={paginaCorrente}'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

righe = soup.find('rows')
nPagine = int(righe.get("num_pages"))
nIterazioni = int(math.ceil(nPagine / 10))

for nPagina in range(2, nPagine):
	decodeURL(nPagina, stringaRicerca)


