from bs4 import BeautifulSoup
from math import ceil
import requests
import time

url = 'https://www.kijiji.it/offerte-di-lavoro/offerta/informatica-e-web/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

out = [] 
for element in soup.find('div', class_='srp-toolbar').find_all('h2', class_='page-hed'):
    out+=element.text.split()
    out.pop(1)

total_announcements_searched = int("".join(c for c in out[0] if c not in ('.')))
total_announcements_per_page = 30

n_pages=ceil(total_announcements_searched/total_announcements_per_page)

with open('announcements.tsv', 'w') as file:
  for i in range(1,n_pages+1):
      print('Page number %d' % i)
      response = requests.get(url, params={'p': i})
      soup = BeautifulSoup(response.text, 'html.parser')
      for element in soup.find('ul', class_='result-list ads-result-list').find_all('li', class_='gtm-search-result'):
          if element.div:
              list_ = {}
              list_[element.get('id')] = {'title': element.div.h3.a.text.strip(),'full_description': element.div.p.text.replace('\n', ' '),
                                         'location': element.div.find('p',class_='locale').text, 'date': element.div.find('p',class_='timestamp').text,
                                         'url': element.div.h3.a.get('href')}
              for announcement in list_.values():
                file.write('%s\t%s\t%s\t%s\t%s\n' % (announcement['title'],announcement['full_description'], announcement['location'], 
                  announcement['date'],announcement['url']))

      time.sleep(1)