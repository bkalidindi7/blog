import sys
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, RadioField
from wtforms.validators import InputRequired
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import sqlite3


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

app.config.update(
   WTF_CSRF_ENABLED = True,
   DEBUG=True,
   SECRET_KEY='c11a678785091b7f1334c24a4123ee75'
)

con = sqlite3.connect('data/players.db', check_same_thread=False)
cursor = con.cursor()

class PlayerSearch(FlaskForm):
    playername = StringField('Player Search', [InputRequired()])

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}

@app.route("/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('index.html', posts=posts)

@app.route('/nba_player_breakdowns', methods=['GET', 'POST'])
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

@app.route('/nba_player_breakdowns/<player_url>', methods=['GET', 'POST'])
def nba_player_breakdowns(player_url):
    #TODO: add data for each year
    return render_template('player_breakdowns.html', url=player_url)

@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
