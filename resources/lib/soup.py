import urllib2
from BeautifulSoup import BeautifulSoup

url = "http://www.deejay.it/reloaded/radio/"

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

prog_list = soup.find('ul', {'class': 'block-grid four-up mobile-two-up'}).findAll('li')

for prog in prog_list :
    print prog
