import math
import requests
import smtplib
from bs4 import BeautifulSoup
from datetime import datetime

trovateNuoveDelibere = False

class Emailer:
    def sendmail(self, recipient, subject, content):
         
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = 587 
        MAIL = ''
        PASSWORD = ''
        #Create Headers
        headers = ["From: " + MAIL, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        #Login to Gmail
        session.login(MAIL, PASSWORD)
 
        #Send Email & Exit
        session.sendmail(MAIL, recipient, headers + "\r\n\r\n" + content)
        session.quit
 
sender = Emailer()

def decodeURL(pagina, stringa):
    URL = f'http://servizissiir.regione.emilia-romagna.it/deliberegiunta/servlet/AdapterHTTP?MODE_VIEW=AJAX&ACTION_NAME=ACTIONRICERCADELIBERE&ENTE=1&tipoAtto=&annoAdozione={datetime.today().year}&numAdozione=&dataAdozioneDa=&dataAdozioneA=&oggetto={stringa}&did=true&POPULATING=LIST&tableId=ricerca_delibere&_=1611778488297&&ricerca_delibere_LIST_PAGE={pagina}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
    rows = soup.find_all('row')
    for riga in rows:
        dataRiga =	datetime.strptime(riga.get('data_adozione_dl'),  '%d/%m/%Y')
        dataCorrente = datetime.today()
        if dataRiga.date() == datetime.today():
            return True
    return False

    
paginaCorrente = 1
stringaRicerca = ''
URL = f'http://servizissiir.regione.emilia-romagna.it/deliberegiunta/servlet/AdapterHTTP?MODE_VIEW=AJAX&ACTION_NAME=ACTIONRICERCADELIBERE&ENTE=1&tipoAtto=&annoAdozione={datetime.today().year}&numAdozione=&dataAdozioneDa=&dataAdozioneA=&oggetto={stringaRicerca}&did=true&POPULATING=LIST&tableId=ricerca_delibere&_=1611778488297&&ricerca_delibere_LIST_PAGE={paginaCorrente}'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

righe = soup.find('rows')
nPagine = int(righe.get("num_pages"))
nIterazioni = int(math.ceil(nPagine / 10))

for nPagina in range(1, nPagine):
    trovateNuoveDelibere = decodeURL(nPagina, stringaRicerca)
for nPagina in range(0, nPagine):
    trovateNuoveDelibere = decodeURL(nPagina + 1, stringaRicerca)
    if trovateNuoveDelibere == True:
        break

if trovateNuoveDelibere == True:
    OggettoMail = f'Messaggio automatico: Trovate nuova delibere per sogliano in data {datetime.today()}'
    sender.sendmail("", OggettoMail, 'vai su http://servizissiir.regione.emilia-romagna.it/deliberegiunta/servlet/AdapterHTTP?action_name=ACTIONRICERCADELIBERE&ENTE=1')
