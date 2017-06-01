from select_players import PlayerSelect
from percentiles import Percentiles
import sys
import sqlite3
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

plyr_sel = PlayerSelect('data/players.db')
perc = Percentiles('data/players.db', plyr_sel)


years = plyr_sel.select('select distinct season from tb_player_info order by season', is_col_lists=True)[1][0]

positions = ['pg', 'sg', 'sf', 'pf', 'c']


"""
Setup data
"""
yrs = str(years[-5:])
pos = positions[-1]
c_scoring_data = []
c_ts_data = []
c_pts_data = []
for yr in years:
    data = perc.data_by_year(yr, ['pts_pgm', 'ts_ptg'], scoring=True)
    c_scoring_data.append(data)
    c_ts_data += data[1][4]
    c_pts_data += data[0][4]

#xs = []
#for d in scoring_data_16[1]:
    #list.sort(d)
    #print len(d)
    #print d
    #xs.append([float(i)/len(d) for i in range(len(d))])
    #print xs[-1]


"""
Plot
"""
# f,a = plt.subplots(4,4)
# a = a.ravel()
arr = np.asarray(c_ts_data)
mu, std = norm.fit(arr)
plt.boxplot(arr)
#plt.hist(arr, bins=len(arr)/5, normed=True, alpha=0.6, color='g')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
#plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()

