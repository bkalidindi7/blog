import numpy as np
import math
import pandas as pd
from urllib2 import urlopen
import string
from bs4 import BeautifulSoup, Comment
import re
import csv
import time

def get_player_links( csv_location ):
    data = pd.read_csv(csv_location)
    headers = list(data.columns.values)
    links = []
    col_size = len(data[headers[0]])
    print col_size
    for i in range(col_size):
        links.append(data['Link'].values[i])
    return links

def find_table(comment_html, table_id ):
    table = comment_html.find('table', id=table_id)
    if (table is not None and len(table) > 0):
        return table
    else:
        return None

def get_table_data( table, column_indexes ):
    if table is None:
        return None
    full_html_td = [r.findAll('td') for r in table.findAll('tr')]
    full_html_a = [r.findAll('a') for r in table.findAll('tr')]
    data = []
    for s in range(1, len(full_html_td) - 1):
        season_with_everything = [full_html_td[s][v].getText().strip() for v in range(len(full_html_td[s]))]
        if (len(season_with_everything) != 0):
            if (season_with_everything[0] == u''):
                break
            season = [season_with_everything[i] for i in range(len(season_with_everything)) if i in column_indexes]
            if len(season) > 0:
                year = full_html_a[s][0].getText()
                if year[:2] == '20' or year[:2] == '19':
                    if int(year[:2]) == 20:
                        season.append(year)
                        data.append(season)
    return data

links = get_player_links('players.csv')
player_stats = []
sleep_count = 0
for link in links:
    url = 'http://www.basketball-reference.com/' + str(link)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    table = soup.find('table', id='per_game')
    per_minute = []
    per_minute_col_indexes = [0, 1, 4, 5, 6, 7, 8, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27]
    advanced = []
    advanced_col_indexes = [7, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26]
    shooting = []
    shooting_col_indexes = range(9,14)+range(15,20)
    pbp = []
    pbp_col_indexes = range(6,11)
    for comment in comments:
        per_minute = per_minute or get_table_data(find_table(BeautifulSoup(comment), 'per_minute'), per_minute_col_indexes)
        advanced = advanced or get_table_data(find_table(BeautifulSoup(comment), 'advanced'), advanced_col_indexes)
        shooting = shooting or get_table_data(find_table(BeautifulSoup(comment), 'shooting'), shooting_col_indexes)
        pbp = pbp or get_table_data(find_table(BeautifulSoup(comment), 'advanced_pbp'), pbp_col_indexes)
    all_stats = [per_minute[i] + advanced[i][:len(advanced[i])-1] + shooting[i][:len(shooting[i])-1] + pbp[i][:len(pbp[i])-1] for i in range(len(per_minute))]
    for r in all_stats:
        r.append(link)
    player_stats.append(all_stats)
    if sleep_count % 5 == 0:
        time.sleep(4)
    sleep_count += 1
    print "Read:" + str(sleep_count) + ',' + link


with open('stats.csv', 'wb') as fp:
    a = csv.writer(fp)
    h = ['Age', 'Team', 'G', 'GS', 'MP', 'FG', 'FGA', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',  'PTS', 'YEAR', 'TS%', 'ORB%', 'DRB%', 'RB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'OWS', 'DWS', 'WS', 'WS48', 'OBPM', 'DBPM', 'BPM', '%FGA_0-2', '%FGA_3-9', '%FGA_10-15', '%FGA_16-3pt', '%FGA_3pt', '%FGP_0-2', '%FGP_3-9', '%FGP_10-15', '%FGP_16-3pt', '%FGP_3pt', '%PG', '%SG', '%SF', '%PF', '%C', 'Link',]
    a.writerow(h)
    write_count = 0
    for player in player_stats:
        for t in player:
            a.writerow(t)
        if write_count % 5 == 0:
            time.sleep(3)
        write_count += 1
        print "Write:",write_count
