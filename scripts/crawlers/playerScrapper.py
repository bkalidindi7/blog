from urllib2 import urlopen
import string
from bs4 import BeautifulSoup
import re
import csv
import time

player_dict = {}
for i in range(2001,2018):
    print i
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(i) + '_per_minute.html?lid=header_seasons'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.findAll('a', attrs={'href': re.compile("^/players/\S/+")}):
        player_dict[a.get('href')] = a.getText() 
    goats = ['/players/a/abdulka01.html','/players/c/chambwi01.html']
    for g in goats:
        del player_dict[g]
    time.sleep(5)
# print player_dict

with open('players_updated.csv', 'wb') as fp:
    a = csv.writer(fp)
    a.writerow(('Link', 'Name'))
    for k in player_dict.keys():
        a.writerow((k, player_dict[k]))


