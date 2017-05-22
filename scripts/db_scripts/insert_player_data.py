import numpy as np
import math
import pandas as pd
from scipy.stats.stats import pearsonr
import sys
import sqlite3

#Open connection
db_loc = sys.argv[1]
players_csv_loc = sys.argv[2]
stats_csv_loc = sys.argv[3]

con = sqlite3.connect(db_loc)
cursor = con.cursor()

#retrieve data from csv for testing
#data is formatted by [[row1][row2],...]
def prepare_data_from_csv( csv_location ):
    data = pd.read_csv(csv_location)
    headers = list(data.columns.values)
    X = []
    col_size = len(data[headers[0]])
    for i in range(col_size):
        row = []
        for h in headers:
            row.append(data[h].values[i])
        X.append(row)
    return headers, X

stats = prepare_data_from_csv(stats_csv_loc)
players = prepare_data_from_csv(players_csv_loc)

#insert data into tb_player
for p in players[1]:
    insert_player = "INSERT INTO tb_player (link, name) VALUES (\"" + p[0] + "\", \"" + p[1] + "\")"
    cursor.execute(insert_player)
    con.commit()

#track tb_player_info pk while iterating
curr_info_id = 0

#insert data into rest of the relations
for s in stats[1]:

    #get player id from tb_player
    select_id = "SELECT player FROM tb_player where link = \"" + s[49] + "\""
    cursor.execute(select_id)
    player_id = cursor.fetchone()[0]

    #insert into tb_player_info
    insert_player_info = "INSERT INTO tb_player_info (player, season, age, team) VALUES (\"" + str(player_id) + "\", \"" + str(s[18]) + "\", \"" + str(s[0]) + "\", \"" + str(s[1]) + "\")"
    cursor.execute(insert_player_info)
    con.commit()
    curr_info_id += 1
    print(curr_info_id)

    #insert into tb_player_played
    insert_player_played = "INSERT INTO tb_player_played (player_info, games_played, games_started, mp) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[2]) + "\", \"" + str(s[3]) + "\", \"" + str(s[4]) + "\")"
    cursor.execute(insert_player_played)
    con.commit()

    #insert into tb_player_shot_selection
    insert_player_shot_selection = "INSERT INTO tb_player_shot_selection (player_info, zero_two_att, three_nine_att, ten_fifteen_att, sixteen_threept_att, threept_att, zero_two_made, three_nine_made, ten_fifteen_made, sixteen_threept_made, threept_att_made) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[34]) + "\", \"" + str(s[35]) + "\", \"" + str(s[36]) + "\", \"" + str(s[37]) + "\", \"" + str(s[38]) + "\", \"" + str(s[39]) + "\", \"" + str(s[40]) + "\", \"" + str(s[41]) + "\", \"" + str(s[42]) + "\", \"" + str(s[43]) + "\")"
    cursor.execute(insert_player_shot_selection)
    con.commit()

    #insert into tb_player_scoring
    insert_player_scoring = "INSERT INTO tb_player_scoring (player_info, pts_pgm, ts_ptg, fg_pg, fga_pg, ft_pg, fta_pg, ft_per) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[17]) + "\", \"" + str(s[19]) + "\", \"" + str(s[5]) + "\", \"" + str(s[6]) + "\", \"" + str(s[7]) + "\", \"" + str(s[8]) + "\", \"" + str(s[9]) + "\")"
    cursor.execute(insert_player_scoring)
    con.commit()

    #insert into tb_player_rebounding
    insert_player_rebounding = "INSERT INTO tb_player_rebounding (player_info, drb_pg, orb_pg, drb_per, orb_per, trb_per) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[11]) + "\", \"" + str(s[10]) + "\", \"" + str(s[21]) + "\", \"" + str(s[20]) + "\", \"" + str(s[22]) + "\")"
    cursor.execute(insert_player_rebounding)
    con.commit()

    #insert into tb_player_passing
    insert_player_passing = "INSERT INTO tb_player_passing (player_info, ast_pg, tov_pg, ast_per, tov_per) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[12]) + "\", \"" + str(s[15]) + "\", \"" + str(s[23]) + "\", \"" + str(s[26]) + "\")"
    cursor.execute(insert_player_passing)
    con.commit()

    #insert into tb_player_defense
    insert_player_defense = "INSERT INTO tb_player_defense (player_info, stl_pg, blk_pg, pf_pg, stl_per, blk_per) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[13]) + "\", \"" + str(s[14]) + "\", \"" + str(s[16]) + "\", \"" + str(s[24]) + "\", \"" + str(s[25]) + "\")"
    cursor.execute(insert_player_defense)
    con.commit()

    #insert into tb_player_position
    insert_player_position = "INSERT INTO tb_player_position (player_info, pg, sg, sf, pf, c) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[44]) + "\", \"" + str(s[45]) + "\", \"" + str(s[46]) + "\", \"" + str(s[47]) + "\", \"" + str(s[48]) + "\")"
    cursor.execute(insert_player_position)
    con.commit()

    #insert into tb_player_adv_misc
    insert_player_adv_misc = "INSERT INTO tb_player_adv_misc (player_info, ows, dws, ws, wsp48, obpm, dbpm, bpm) VALUES (\"" + str(curr_info_id) + "\", \"" + str(s[27]) + "\", \"" + str(s[28]) + "\", \"" + str(s[29]) + "\", \"" + str(s[30]) + "\", \"" + str(s[31]) + "\", \"" + str(s[32]) + "\", \"" + str(s[33]) + "\")"
    cursor.execute(insert_player_adv_misc)
    con.commit()

cursor.close()
con.close()
