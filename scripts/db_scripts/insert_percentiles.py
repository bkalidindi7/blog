from select_players import PlayerSelect
from percentiles import Percentiles
import sys
import sqlite3

perc = Percentiles('data/players.db')
plyr_sel = PlayerSelect('data/players.db')
# scoring_query = ps.pos_stats_by_table(pos='c', scoring=True, min_mp=600)
# l = ps.select(scoring_query, is_col_lists=False)
# print("Desc: ", l[0])
# print("Data: ", l[1][0])
years = range(2000, 2016)
positions = ['pg', 'sg', 'sf', 'pf', 'c']

yr = years[-1]
pos = positions[-1]
scoring_data = plyr_sel.pos_stats_by_table(pos=pos, scoring=True)
