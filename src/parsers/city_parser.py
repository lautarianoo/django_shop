

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'}
]

CITIES = [

]

def city_pars(url):
    errors = []
    total = 0
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            table = soup.find('table', attrs={})
            td_list = table.find_all('td', attrs={})
            if table:
                for td in td_list:
                    total +=1
                    text = td.text
                    CITIES.append((f"{total}", f"{text}"))
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page you not response'})
        return errors

if __name__ == '__main__':
    url = 'http://www.statdata.ru/largest_cities_russia'
    city_pars(url)
    del CITIES[0:10]
    del CITIES[118:-1]