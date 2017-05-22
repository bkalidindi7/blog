from select_players import PlayerSelect
import sys
from scipy.stats import percentileofscore

ps = PlayerSelect(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5])
select_scoring_prefix = "select tpi.player_info, tps.pts_pgm, tps.ts_ptg, tps.fg_pg, tps.fga_pg, tps.ft_pg, tps.fta_pg, tps.ft_per"
#common_pos_selects = ", pos.pg, pos.sg, pos.sf, pos.pf, pos.c"
common_joins = " from tb_player_played tpp join tb_player_info tpi on tpi.player_info = tpp.player_info join tb_player_position pos on pos.player_info = tpp.player_info"
scoring_join = " JOIN tb_player_scoring tps on tps.player_info = tpp.player_info"
common_where = " where mp > 600 and season = %s"
pos_cond = " and pos.c > .33"
scoring_query = select_scoring_prefix + common_joins + scoring_join + common_where + pos_cond
#print scoring_query
print ps.pos_stats_by_table(pos='c', scoring=True, min_mp=600)
#l = ps.select(scoring_query, params=['2015-16'], is_col_lists=True)
#print("Desc: ", l[0])
#print("Data: ", l[1][0])
#percentileofscore