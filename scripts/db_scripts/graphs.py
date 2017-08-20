from select_players import PlayerSelect
from percentiles import Percentiles
import sys
import sqlite3
import matplotlib.pyplot as plt
from scipy.stats import norm, skew, skewtest, zscore
import probscale
import numpy as np
import pylab
# import statsmodels.api as sm

def create_boxplot(l_data, a_min, a_max, num_plots, id_plt, title, has_label=False):
    ax = plt.subplot(1,num_plots, id_plt)
    length = len(l_data)
    arr = np.asarray(l_data)
    # Finding stats
    mu, std = norm.fit(arr)
    mu = np.mean(arr)
    std = np.std(arr)
    med = np.median(arr)
    sk = skew(arr)
    z,p = skewtest(arr)
    stats = "%s: mu=%.3f, md=%.3f, sd=%.3f, skew=%.3f, p=%.3f, len=%.3f" % (title, mu, med, std, sk, p, length)
    print stats
    # Making boxplot
    ax.boxplot(arr, 0)
    # Setting min and max of each plot
    ax.set_ylim([a_min, a_max])
    ax.set_title(title)
    # For removing labels for all but first graph
    # if i == 0: plt.ylabel('TS%')
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    if not has_label:
        frame1.axes.get_yaxis().set_visible(False)
    return ax


plyr_sel = PlayerSelect('data/players.db')
perc = Percentiles('data/players.db', plyr_sel)

# TO-DO: functionalize code
attrs = ['pts_pgm', 'ts_ptg']

    
"""
Setup data
"""
span_length = 1
years = plyr_sel.select('select distinct season from tb_player_info order by season', is_col_lists=True)[1][0]
# years = ['2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

# Data per year will go here. ex: ts = d_y[1], ts['2014-15']['pg']
d_y = [ {} for a in attrs]


# spans = zip(years, years[1:], years[2:], years[3:])
spans = [years[i:i+4] for i in range(0, len(years), 4)]

positions = ['pg', 'sg', 'sf', 'pf', 'c']
pos_dict = {positions[i] : i for i in range(len(positions))}

pts_data = []

for yr in years:
    # Yearly data organized by attr then pos
    data = perc.data_by_year(yr, attrs, scoring=True)
    # Iterate by attr to add to yearly keyed dict for positional data
    for a in range(len(attrs)):
        p_d = { positions[i]: data[a][i] for i in range(len(positions))}
        d_y[a][yr] = p_d


"""
Plot
"""

fig = plt.figure()


# Go through each position
for p in positions:
    # Go through each attribute
    for i in range(len(attrs)):
        fig = plt.figure()
        # Dictionary fo data for specific attr; keys are year
        all_attr_data = d_y[i]
        attr_max = float("-inf")
        attr_min = float("inf")
        id_plt = 1
        print "\n" + p + ": " + attrs[i]
        graph_data = []
        titles = []

        for span in spans:
            # Data for one of the plots in figure
            plot_data = []
            for yr in span:
                plot_data += all_attr_data[yr][p]
            attr_max = max(max(plot_data), attr_max)
            attr_min = min(min(plot_data), attr_min)
            title = span[0][5:] + span[-1][4:]
            titles.append(title)
            num_plots = len(spans)
            graph_data.append(plot_data)

        file_loc = "content/stats_plots/"

        # Boxplot
        for y in range(len(graph_data)):
            subplot = create_boxplot(graph_data[y], attr_min, attr_max, num_plots, y+1, titles[y], has_label=y==0)
            fig.add_subplot(subplot)
        fig.savefig(file_loc + p + "_" + attrs[i] + "_box" + ".png", dpi=100)

        # QQ
        fig_prob, axs_prob = plt.subplots(figsize=(9, 6), ncols=len(graph_data), sharex=True)
        for y in range(len(graph_data)):

            z_list = zscore(np.array(graph_data[y]))

            ax = axs_prob[y]

            ax.grid(False)
            ax.set_title(titles[y])
            fig_prob = probscale.probplot(z_list, plottype='qq', ax=ax)
            ax.plot([-4,4],[-4,4])

            # z_list = zscore(np.array(graph_data[y]))
            # fig_prob = sm.qqplot(z_list, line='45')

        fig_prob.savefig(file_loc + p + "_" + attrs[i] + "_qq" + ".png", dpi=100)

        print "Max:", attr_max
        print "Min:", attr_min


