from select_players import PlayerSelect
import sys
from scipy.stats import percentileofscore
import sqlite3

class Percentiles:

    def __init__(self, db_loc, ps):
        self.db_loc = db_loc
        self.ps = ps
        self.possible_pos = ['pg', 'sg', 'sf', 'pf', 'c']

    def attr_player_percentile(self, player_info_num, data, player_stat):
        """
        param player_info_num: id in tb_player_info
        param data: data at each position in order of pg, sg, sf, pf, c
        param player_stat: players stat within data
        returns: player's average position, player's percentile within the data
        """
        positions, player_pos = self.ps.player_positions(player_info_num)
        percentile = 0
        for i in range(len(positions)):
            if positions[i] > 0:
                pos_percentile = (percentileofscore(data[i], player_stat))
                print("POS: ",i)
                print(pos_percentile)
                print(positions[i])
                print('\n')
                percentile += positions[i] * pos_percentile
        return player_pos, percentile

    def data_by_year(self, yr, attrs, advanced=False, defense=False, passing=False, reb=False, scoring=False, shot_sel=False):
        """
        param yr: year to get data
        param advanced, defense, passing, reb, scoring, shot_sel: choose table
        param attrs: which attributes in table to find percentiles
        returns: attribute data at each position at specified year: returned_list[attr][pos]
        """
        ind = []
        total_data = []

        # attr_perc = [[] for a in attrs]
        # player_info_query = "select player_info from tb_player_info"
        # player_infos = self.ps.select(player_info_query, is_col_lists=True)
        
        for attr in attrs:
            pos_data = []
            for pos in self.possible_pos:
                data = self.ps.pos_stats_by_table(pos=pos, advanced=advanced, defense=defense, passing=passing, reb=reb, scoring=scoring, shot_sel=shot_sel, year=yr, attrs=[attr])[1]
                pos_data.append(data[0])
            total_data.append(pos_data)
        # for player in player_infos:
        #     # TODO: Get player_stat
        #     for attr_data in total_data
        #         attr_player_percentile(player, attr_data, player_stat)


        return total_data
        # return player_infos, attr_perc
