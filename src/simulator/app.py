#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run all simulations and create the graphs
# Author: Claudio Sousa, David Gonzalez
#

from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PlayerStopAt import PlayerStopAt
from PlayerKOCount import PlayerKOCount
from simulator import playGame
import numpy as np
RUNS = 10000
PLAYERS = 7

croupier = PlayerStopAt(17)
strategies = [[PlayerStopAt(x)]+[PlayerKOCount(x)] for x in range(8, 22)]
strategies = np.array(strategies).flatten()
# % win for the last player for a variable number of players
g1_sum_win = [[0] * PLAYERS for _ in strategies]

for _ in range(RUNS):
    for s_i, s in enumerate(strategies):
        for p in range(PLAYERS):
            c_result, p_result, c_cards = playGame(croupier, [s] * (p + 1))
            g1_sum_win[s_i][p] += p_result[-1]

pprint(g1_sum_win)

# % win for all players with 7 in the game
g2_sum_win = [[0] * PLAYERS for _ in strategies]

for _ in range(RUNS):
    for s_i, s in enumerate(strategies):
        c_result, p_result, c_cards = playGame(croupier, [s for _ in range(PLAYERS)])
        for res_i, res in enumerate(p_result):
            g2_sum_win[s_i][res_i] += p_result[res_i]

pprint(g2_sum_win)

# % win for different strategies of stopAt
g3_sum_win = [[0] * 10 for _ in strategies]

for _ in range(RUNS):
    for s_i, s in enumerate(strategies):
        c_result, p_result, c_cards = playGame(croupier, [s])
        g3_sum_win[s_i][c_cards[0] - 2] += p_result[0]

pprint(g3_sum_win)

# Normalise data
g1_sum_win = [[(v + RUNS) / (RUNS * 2) for v in w] for w in g1_sum_win]
g2_sum_win = [[(v + RUNS) / (RUNS * 2) for v in w] for w in g2_sum_win]
g3_sum_win = [[(v + RUNS) / (RUNS * 2) for v in w] for w in g3_sum_win]

pprint(g1_sum_win)
pprint(g2_sum_win)
pprint(g3_sum_win)

# First graph on % win of last player
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for s_i, s in enumerate(strategies):
    ax.bar3d(s_i, range(1, PLAYERS + 1), [0] * len(g1_sum_win[s_i]), 1, 1, g1_sum_win[s_i])
# ax.set_zlim3d(0, 1)
ax.set_title("Win rate of the last player for different number of player")
ax.set_xlabel("Strategies")
ax.set_ylabel("Number of player")
ax.set_zlabel("Win rate for last player")
plt.sca(ax)
plt.xticks(range(len(strategies)), [s for s in strategies], rotation=90)

# Second graph on % win of all player
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for s_i, s in enumerate(strategies):
    ax.bar3d(s_i, range(1, PLAYERS + 1), [0] * len(g2_sum_win[s_i]), 1, 1, g2_sum_win[s_i])
# ax.set_zlim3d(0, 1)
ax.set_title("Players win rate per position in games with 7 players")
ax.set_xlabel("Strategies")
ax.set_ylabel("Position of player")
ax.set_zlabel("Win rate")
plt.sca(ax)
plt.xticks(range(len(strategies)), [s for s in strategies], rotation=90)

# Third graph on % win of different strategies of StopAt
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for s_i, s in enumerate(strategies):
    ax.bar3d(s_i, range(2, 12), [0] * len(g3_sum_win[s_i]), 1, 1, g3_sum_win[s_i])
# ax.set_zlim3d(0, 1)
ax.set_title("Player win rate according to first initial card of the croupier")
ax.set_xlabel("Strategies")
ax.set_ylabel("First initial card of croupier")
ax.set_zlabel("Win rate")
plt.sca(ax)
plt.xticks(range(len(strategies)), [s for s in strategies], rotation=90)

plt.show()
