from select_players import PlayerSelect
from percentiles import Percentiles
import sys
import sqlite3
import matplotlib.pyplot as plt
from scipy.stats import norm, skew, skewtest
import numpy as np

plyr_sel = PlayerSelect('data/players.db')
perc = Percentiles('data/players.db', plyr_sel)

# TO-DO: functionalize code
"""
Setup data
"""
span_length = 4
years = plyr_sel.select('select distinct season from tb_player_info order by season', is_col_lists=True)[1][0]
spans = [years[i:i+span_length] for i in range(0, len(years), span_length)]
positions = ['pg', 'sg', 'sf', 'pf', 'c']


"""
scoring_data holds all data from 01-16 for each position indexed by time (either year or span), attribute, then position
ts_data and pts_data hold all data from all years for a specific position
"""
yr_scoring_data = []
ts_data = []
pts_data = []
spans_scoring_data = []
attrs = ['pts_pgm', 'ts_ptg']

for span in spans:
    span_data = [ [ [] for p in positions] for a in attrs]
    for yr in span:
        data = perc.data_by_year(yr, attrs, scoring=True)
        yr_scoring_data.append(data)
        ts_data += data[1][4]
        pts_data += data[0][4]
        for a in range(len(attrs)):
            for pos in range(len(positions)):
                span_data[a][pos] += data[a][pos]
    spans_scoring_data.append(span_data)

# print spans_scoring_data[0]
# print yr_scoring_data[0:4]


"""
Plot
"""
c = 4
pf = 3
sf = 2
sg = 1
pg = 0

ts = 1
ppg = 0

for i in range(len(spans_scoring_data)):
    ax = plt.subplot(1,len(years)/span_length,i+1)
    data = spans_scoring_data[i][ts][pg]

    arr = np.asarray(data)
    # Finding stats
    mu, std = norm.fit(arr)
    mu = np.mean(arr)
    std = np.std(arr)
    med = np.median(arr)
    sk = skew(arr)
    z,p = skewtest(arr)
    year_title = years[i*span_length][-2:] + "-" + years[span_length*i+(span_length-1)][-2:]
    stats = "%s: mu=%.3f, md=%.3f, sd=%.3f, skew=%.3f" % (year_title, mu, med, std, sk)
    print stats
    # Making boxplot
    ax.boxplot(arr, 0)
    # Setting min and max of each plot
    ax.set_ylim([min(ts_data), max(ts_data)])
    ax.set_title(year_title)
    # For removing labels for all but first graph
    if i == 0: plt.ylabel('PPG')
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    if i != 0:
        frame1.axes.get_yaxis().set_visible(False)

plt.show()

