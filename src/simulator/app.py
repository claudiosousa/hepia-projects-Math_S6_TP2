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

RUNS = 100
PLAYERS_NB = 7
PLAYERS = list(range(1, PLAYERS_NB + 1))
WINRATE_TYPE_NB = 5
CARDS = list(range(2, 12))
CARDS_TYPE_NB = len(CARDS)
CROUPIER = PlayerStopAt(17)
STOP_AT_VALUES = list(range(11, 22))
STOP_AT_BEST = 17
STRATEGIES = [PlayerStopAt, PlayerKOCount]

# Data of graph 1
g1_runs = RUNS
g1_strategies = [PlayerStopAt(x) for x in STOP_AT_VALUES]
g1_sum_win = [[0] * WINRATE_TYPE_NB for _ in g1_strategies]

for _ in range(g1_runs):
    for s_i, s in enumerate(g1_strategies):
        c_result, p_result, c_cards = playGame(CROUPIER, [s])
        g1_sum_win[s_i][0] += p_result[0]

# Data of graph 2
g2_runs = RUNS
g2_strategies = [[PlayerStopAt(x) for x in STOP_AT_VALUES], [PlayerKOCount(x) for x in STOP_AT_VALUES]]
g2_sum_win = [[0] * len(s) for s in g2_strategies]

for _ in range(g2_runs):
    for st_i, st in enumerate(g2_strategies):
        for s_i, s in enumerate(st):
            c_result, p_result, c_cards = playGame(CROUPIER, [s])
            g2_sum_win[st_i][s_i] += p_result[0]

# Data of graph 3
g3_runs = RUNS
g3_strategies = [PlayerStopAt(STOP_AT_BEST), PlayerKOCount(STOP_AT_BEST)]
g3_sum_win = [[0] * CARDS_TYPE_NB for _ in g3_strategies]

for _ in range(g3_runs):
    for s_i, s in enumerate(g3_strategies):
        c_result, p_result, c_cards = playGame(CROUPIER, [s])
        g3_sum_win[s_i][c_cards[0] - 2] += p_result[0]

# Data of graph 4
g4_runs = RUNS
g4_strategies = [PlayerStopAt(STOP_AT_BEST), PlayerKOCount(STOP_AT_BEST)]
g4_sum_win = [[0] * PLAYERS_NB for _ in g3_strategies]

for _ in range(g4_runs):
    for s_i, s in enumerate(g3_strategies):
        c_result, p_result, c_cards = playGame(CROUPIER, [s] * PLAYERS_NB)
        for res_i, res in enumerate(p_result):
            g4_sum_win[s_i][res_i] += res

print()

# Normalise data
g1_sum_win = [[(v + g1_runs) / (g1_runs * 2) for v in w] for w in g1_sum_win]
g2_sum_win = [[(v + g2_runs) / (g2_runs * 2) for v in w] for w in g2_sum_win]
g3_sum_win = [[(v + g3_runs) / (g3_runs * 2) for v in w] for w in g3_sum_win]
g4_sum_win = [[(v + g4_runs) / (g4_runs * 2) for v in w] for w in g4_sum_win]

# Graph 1:
fig = plt.figure()
ax = fig.add_subplot(111)

ax.grid()
ax.set_title("Area for each rate per StopAt values for different strategies in " + str(g1_runs) + " runs")
ax.set_xlabel("StopAt values")
ax.set_ylabel("Win rate")
ax.legend()

# Graph 2:
fig = plt.figure()
ax = fig.add_subplot(111)
for s_i, w in enumerate(g2_sum_win):
    ax.plot(STOP_AT_VALUES, w, '-', linewidth=2, label=STRATEGIES[s_i].__name__)
    for x, y in zip(STOP_AT_VALUES, w):
        ax.text(x, y, f'{y}')
ax.grid()
ax.set_title("Win rate per StopAt values for different strategies in " + str(g2_runs) + " runs")
ax.set_xlabel("StopAt values")
ax.set_ylabel("Win rate")
ax.legend()

# Graph 3:
fig = plt.figure()
ax = fig.add_subplot(111)
for s_i, w in enumerate(g3_sum_win):
    ax.plot(CARDS, w, '-', linewidth=2, label=g3_strategies[s_i])
    for x, y in zip(CARDS, w):
        ax.text(x, y, f'{y}')
ax.grid()
ax.set_title("Win rate per initial card of the croupier for best strategies in " + str(g3_runs) + " runs")
ax.set_xlabel("Croupier's initial card")
ax.set_ylabel("Win rate")
ax.legend()

# Graph 4:
fig = plt.figure()
ax = fig.add_subplot(111)
for s_i, w in enumerate(g4_sum_win):
    ax.plot(PLAYERS, w, '-', linewidth=2, label=g4_strategies[s_i])
    for x, y in zip(PLAYERS, w):
        ax.text(x, y, f'{y}')
ax.grid()
ax.set_title("Win rate per player position for best strategies in " + str(g4_runs) + " runs")
ax.set_xlabel("Player position")
ax.set_ylabel("Win rate")
ax.legend()

plt.show()
