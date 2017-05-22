from select_players import PlayerSelect
import sys
from scipy.stats import percentileofscore
import sqlite3

class Percentiles:

    def __init__(self, db_loc):
        self.db_loc = db_loc

    def complete_player_percentiles(self, player_info_num, data):
        ps = PlayerSelect(self.db_loc)
        positions = ps.player_positions(player_info_num)
        pos = 1*positions[0] + 2*positions[1] + 3*positions[2] + 4*positions[3] + 5*positions[4]
        pos_stats_by_table
        # Not Finished