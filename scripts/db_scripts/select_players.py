import pymysql
import numpy as np
import math
import pandas as pd
from scipy.stats.stats import pearsonr
import sys
pymysql.install_as_MySQLdb()

class PlayerSelect:
    """
    Class for selecting players from the database
    """
    def __init__(self, host, user, port, password, db):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.db = db

    def select(self, query, params=None, is_col_lists=False):
        """
        Select player data using query, and return in a list of columns
        """
        #Connect to DB
        con = pymysql.connect(host=self.host, user=self.user, port=self.port, passwd=self.password, db=self.db)
        cursor = con.cursor()
        #Execute query
        if params:
            cursor.execute(query, params)
        else:
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

    def pos_stats_by_table(self, pos='pg', advanced=False, defense=False, passing=False, reb=False, scoring=False, shot_sel=False, min_mp=0, year='2015-16'):
        table = ''
        if advanced: table = 'adv_misc'
        if defense: table = 'defense'
        if passing: table = 'passing'
        if reb: table = 'rebounding'
        if scoring: table = 'scoring'
        if shot_sel: table = 'shot_selection'

        select = "select " + table + ".*"
        common_joins = " from tb_player_played tpp join tb_player_info tpi on tpi.player_info = tpp.player_info" \
                       " join tb_player_position pos on pos.player_info = tpp.player_info"
        attr_table_join = " join tb_player_" + table + " " + table + " on " + table + ".player_info = tpp.player_info"
        where = " where mp > " + str(min_mp) + " and season = '" + year + "' and pos." + pos + " > .33"
        query = select + common_joins + attr_table_join + where
        return query