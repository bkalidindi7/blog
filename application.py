import sys
from scripts.db_scripts.percentiles import Percentiles
from scripts.db_scripts.select_players import PlayerSelect
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, RadioField
from wtforms.validators import InputRequired
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import sqlite3
import math
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

application = Flask(__name__)
flatpages = FlatPages(application)
freezer = Freezer(application)
application.config.from_object(__name__)

application.config.update(
   WTF_CSRF_ENABLED = True,
   DEBUG=True,
   SECRET_KEY='c11a678785091b7f1334c24a4123ee75'
)

con = sqlite3.connect('data/players.db', check_same_thread=False)
cursor = con.cursor()

class PlayerSearch(FlaskForm):
    playername = StringField('Player Search', [InputRequired()])

@application.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}

@application.route("/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    return render_template('index.html', posts=posts)

@application.route('/nba_player_breakdowns', methods=['GET', 'POST'])
def nba_breakdowns():
    form = PlayerSearch()
    name_html = ''
    if form.validate_on_submit():
        playername = form.playername.data
        select_query = "select name, player from tb_player where name like '%" + playername + "%'"
        cursor.execute(select_query)
        players = cursor.fetchall()
        for player in players:
            name_html += '<p align="center"> <a href="{}"> {} </a></p>'.format(url_for('nba_player_breakdowns', player_url=player[1]), player[0])

    return render_template('nba_breakdowns.html', title='Search', form=form, name_html=name_html)

@application.route('/nba_player_breakdowns/<player_url>', methods=['GET', 'POST'])
def nba_player_breakdowns(player_url):

    plyr_sel = PlayerSelect('data/players.db')
    perc = Percentiles('data/players.db', plyr_sel)

    name_query = 'select name from tb_player where player = ' + str(player_url)
    player_infos_query = 'select player_info, season, team from tb_player_info where player = ' + str(player_url)
    name = plyr_sel.select(name_query)[1][0][0]
    pis, seasons, teams = plyr_sel.select(player_infos_query, is_col_lists=True)[1]

    scoring_headers = ['Season', 'Team', 'Points', 'True Shooting', 'FGA', 'FTA', 'FT%']
    scoring_html = "<table><caption>Scoring</caption><tr>"
    for sh in scoring_headers:
        scoring_html += "<th>" + sh + "</th>"
    scoring_html += "</tr>"
    for i in range(len(seasons)):
        scoring_html += "<tr>"
        scoring_html += "<td>" + seasons[i] + "</td>"
        scoring_html += "<td>" + teams[i] + "</td>"
        scoring_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'pts_pgm') + "</td>"
        scoring_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'ts_ptg') + "</td>"
        scoring_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'fga_pg') + "</td>"
        scoring_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'fta_pg') + "</td>"
        scoring_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'ft_per') + "</td>"
        scoring_html += "</tr>"

    reb_headers = ['Season', 'Team', 'DRB', 'ORB', 'TRB']
    reb_html = "<table><caption>Rebounding</caption><tr>"
    for rh in reb_headers:
        reb_html += "<th>" + rh + "</th>"
    reb_html += "</tr>"
    for i in range(len(seasons)):
        reb_html += "<tr>"
        reb_html += "<td>" + seasons[i] + "</td>"
        reb_html += "<td>" + teams[i] + "</td>"
        reb_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'drb_per') + "</td>"
        reb_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'orb_per') + "</td>"
        reb_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'trb_per') + "</td>"
        reb_html += "</tr>"

    pass_headers = ['Season', 'Team', 'AST', 'TOV']
    pass_html = "<table><caption>Passing</caption><tr>"
    for ph in pass_headers:
        pass_html += "<th>" + ph + "</th>"
    pass_html += "</tr>"
    for i in range(len(seasons)):
        pass_html += "<tr>"
        pass_html += "<td>" + seasons[i] + "</td>"
        pass_html += "<td>" + teams[i] + "</td>"
        pass_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'ast_per') + "</td>"
        pass_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'tov_per') + "</td>"
        pass_html += "</tr>"

    def_headers = ['Season', 'Team', 'STL', 'BLK', 'PF', 'DBPM']
    def_html = "<table><caption>Defense</caption><tr>"
    for dh in def_headers:
        def_html += "<th>" + dh + "</th>"
    def_html += "</tr>"
    for i in range(len(seasons)):
        def_html += "<tr>"
        def_html += "<td>" + seasons[i] + "</td>"
        def_html += "<td>" + teams[i] + "</td>"
        def_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'stl_per') + "</td>"
        def_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'blk_per') + "</td>"
        def_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'pf_pg') + "</td>"
        def_html += "<td>" + "%.2f" % perc.attr_player_percentile(pis[i], 'dbpm') + "</td>"
        def_html += "</tr>"




    return render_template('player_breakdowns.html', name=name, scoring_html=scoring_html, reb_html=reb_html, pass_html=pass_html, def_html=def_html)

@application.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        application.run(host='0.0.0.0', debug=True)
