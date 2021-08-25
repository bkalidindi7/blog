title: Our NBA Player Breakdown Tool
date: 2017-08-21

<!-- <iframe align="center" width="280" height="155" src="https://www.youtube.com/embed/9ziXpIPAhD4" frameborder="0" allowfullscreen></iframe> -->

Consider two NBA players, Player A and Player B, with the following assists and turnover stats in the past season:

<table>
    <tr>
        <th></th>
        <th>Assists Per Game</th>
        <th>Turnovers Per Game</th>
    </tr>
    <tr>
        <td>Player A</td>
        <td>10.4</td>
        <td>5.4</td>
    </tr>
    <tr>
        <td>Player B</td>
        <td>3.5</td>
        <td>2.1</td>
    </tr>
</table>



Having a complete view of the most important box score stats available, it appears Player A is the superior passer due to such high assist numbers (even with the high number of turnovers). However, there is are key pieces of information that has been witheld. We have no way of understanding how impressive or unimpressive each of these stats are in comparison to other players at the same position, and we don't know how many possessions it took for these players to accumulate such stats. Looking at per game stats such as these makes it difficult to interpret the average boxscore for players.

We've built a [tool](/nba_player_breakdowns) for converting these stats into percentiles. Meaning, we look at these same stats, normalize them by either minutes or possessions, and identify what percentile it falls under in comparison to all other players at the position that player plays. The tool can be found under the NBA Player Analysis tab on the menu bar at the top, and contains all player data from 2001, when play by play data became avaiable. Using this tool, you might find some interesting information, such as Tim Duncan sporting a suprisingly mediocre shooting efficiency (although he made up for it with elite performance in every other aspect of the game), and Allen Iverson grading out as a sneaky good defender (in his prime). A higher percentile is always better, so for stats such as turnovers and fouls, a higher percentile indicates low values.

Going back to the original comparison between Player A and Player B: here's how they grade out in terms of assists and turnovers using our tool:

<table>
    <tr>
        <th></th>
        <th>Assists Percentile</th>
        <th>Turnovers Percentile</th>
    </tr>
    <tr>
        <td>Player A</td>
        <td>100.00</td>
        <td>34.32</td>
    </tr>
    <tr>
        <td>Player B</td>
        <td>91.09</td>
        <td>73.79</td>
    </tr>
</table>


Player A's stats seem to hold true to our original interpretation. A high percentage of his possessions result in assists, as well as turnovers, in comparison to other players at his position. However, Player B seems to be an elite playmaker in his own right as his position, passing the ball well while doing a good job of limiting turnovers.

Player A is Russell Westbrook, the past season's MVP, and Player B is Kawhi Leonard, who finished 3rd. One of the reasons Westbrook got the advantage over Leonard was his supposed elite playmaking compared to Leonard supposed mediocre playmaking. However, we can now see that Leonard was actually a great playmaker as well. He just doesn't play point guard like Westbrook, and doesn't have the ball in his hands as much of the time. But among small forwards, Leonard was great at making the most of his possessions.

