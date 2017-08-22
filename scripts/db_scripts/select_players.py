import pandas as pd
import numpy as np
import math
from scipy.stats.stats import pearsonr
import sys
import sqlite3

class PlayerSelect:

    """
    Class for selecting players from the database
    """
    def __init__(self, db_loc):
        self.db_loc = db_loc
        self.scoring_attr = ['pts_pgm', 'ts_ptg', 'fg_pg', 'fga_pg', 'ft_pg', 'fta_pg', 'ft_per']
        self.reb_attr = ['drb_per', 'orb_per', 'trb_per', 'drb_pg', 'orb_pg']
        self.passing_attr = ['ast_per', 'tov_per', 'ast_pg', 'tov_pg']
        self.shot_sel_attr = ['zero_two_att', 'three_nine_att', 'ten_fifteen_att', 'sixteen_threept_att', 'threept_att', 'zero_two_made', 'three_nine_made', 'ten_fifteen_made', 'sixteen_threept_made', 'threept_att_made']
        self.def_attr = ['stl_pg', 'blk_pg', 'pf_pg', 'stl_per', 'blk_per']
        self.adv_attr = ['ows', 'dws', 'ws', 'wsp48', 'obpm', 'dbpm', 'bpm']

        self.attr_table_dict = {}
        for s in self.scoring_attr:
            self.attr_table_dict[s] = 'scoring'
        for s in self.reb_attr:
            self.attr_table_dict[s] = 'rebounding'
        for s in self.passing_attr:
            self.attr_table_dict[s] = 'passing'
        for s in self.shot_sel_attr:
            self.attr_table_dict[s] = 'shot_shot_selection'
        for s in self.def_attr:
            self.attr_table_dict[s] = 'defense'
        for s in self.adv_attr:
            self.attr_table_dict[s] = 'adv_misc'


    def select(self, query, is_col_lists=False):
        """
        Select player data using query, and return in a list of columns
        """
        #Connect to DB
        con = sqlite3.connect(self.db_loc, check_same_thread=False)
        cursor = con.cursor()
        #Execute query
        cursor.execute(query)
        desc = [d[0] for d in cursor.description]
        data = cursor.fetchall()
        #Make into list of columns
        if is_col_lists:
            cols = []
            for i in range(len(desc)):
                cols.append([])
            for r in data:
                for i in range(len(desc)):
                    cols[i].append(r[i])
            data = cols
        #Close connection and return
        cursor.close()
        con.close()
        return desc, data


    def pos_stats_by_table(self, pos='pg', table='scoring', min_mp=600, year='2015-16', attrs=None):

        select = "select " + table + ".*"
        if attrs:
            select = "select "
            for attr in attrs[:len(attrs)-1]:
                select += table + "." + attr + ", "
            select += table + "." + attrs[len(attrs)-1]
        
        common_joins = " from tb_player_played tpp join tb_player_info tpi on tpi.player_info = tpp.player_info" \
                       " join tb_player_position pos on pos.player_info = tpp.player_info"
        attr_table_join = " join tb_player_" + table + " " + table + " on " + table + ".player_info = tpp.player_info"
        where = " where mp > " + str(min_mp) + " and season = '" + year + "' and pos." + pos + " > .33"
        query = select + common_joins + attr_table_join + where
        desc, data = self.select(query, is_col_lists=True)
        return desc, data


    def player_positions(self, player_info_num):
        query = "select pg, sg, sf, pf, c from tb_player_position where player_info = " + str(player_info_num)
        data = self.select(query)
        positions = data[1][0]
        player_pos = 1*positions[0] + 2*positions[1] + 3*positions[2] + 4*positions[3] + 5*positions[4]
        return positions, player_pos