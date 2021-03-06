#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run all simulations and create the graphs
# Author: Claudio Sousa, David Gonzalez
#

from pprint import pprint
import matplotlib.pyplot as plt
from PlayerStopAt import PlayerStopAt
from PlayerKOCount import PlayerKOCount
from simulator import playGame
import numpy as np

RUNS = 100000
PLAYERS_NB = 7
PLAYERS = list(range(1, PLAYERS_NB + 1))
WINRATE_TYPE_NB = 5
CARDS = list(range(2, 12))
CARDS_TYPE_NB = len(CARDS)
CROUPIER = PlayerStopAt(17)
STOP_AT_VALUES = list(range(11, 22))
STOP_AT_BEST = 17
STRATEGIES = [PlayerStopAt, PlayerKOCount]
TEXTCOLORS = ["#175885", "#753A06"]

# Data of graph 1
g1_runs = RUNS
g1_strategies = [PlayerStopAt(x) for x in STOP_AT_VALUES]
g1_sum_win = [[0] * WINRATE_TYPE_NB for _ in g1_strategies]

for _ in range(g1_runs):
    for s_i, s in enumerate(g1_strategies):
        c_result, p_result, p_died, c_cards = playGame(CROUPIER, [s])
        res = p_result[0]
        died = p_died[0]

        if res > 0: # win
            g1_sum_win[s_i][0 if died == 0 else 1] += 1
        elif res < 0: # lose
            g1_sum_win[s_i][3 if died == 0 else 4] += 1
        else: # draw
            g1_sum_win[s_i][2] += 1

# Data of graph 2
g2_runs = RUNS
g2_strategies = [PlayerStopAt(STOP_AT_BEST)]
g2_sum_win = [[0] * CARDS_TYPE_NB for _ in g2_strategies]

for _ in range(g2_runs):
    for s_i, s in enumerate(g2_strategies):
        c_result, p_result, p_died, c_cards = playGame(CROUPIER, [s])
        g2_sum_win[s_i][c_cards[0] - 2] += p_result[0]

# Data of graph 3
g3_runs = RUNS
g3_strategies = [[PlayerStopAt(x) for x in STOP_AT_VALUES], [PlayerKOCount(x) for x in STOP_AT_VALUES]]
g3_sum_win = [[0] * len(s) for s in g3_strategies]

for _ in range(g3_runs):
    for st_i, st in enumerate(g3_strategies):
        for s_i, s in enumerate(st):
            c_result, p_result, p_died, c_cards = playGame(CROUPIER, [s])
            g3_sum_win[st_i][s_i] += p_result[0] if p_result[0] != 0 else 1

# Normalise data
g1_sum_win = [[v / g1_runs for v in w] for w in g1_sum_win]
g2_sum_win = [[(v + g2_runs) / (g2_runs * 2) for v in w] for w in g2_sum_win]
g3_sum_win = [[(v + g3_runs) / (g3_runs * 2) for v in w] for w in g3_sum_win]

# Graph 1:
g1_colors =  [(1.0, 1.0, 0.0), (1.0, 0.8, 0.0), (0.6, 0.6, 0.6), (0.0, 1.0, 1.0), (0.0, 0.8, 1.0)]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.stackplot(STOP_AT_VALUES, list(map(list, zip(*g1_sum_win))), colors=g1_colors)
for x, w in zip(STOP_AT_VALUES, g1_sum_win):
    y_sum = 0
    for y in w:
        ax.text(x, y_sum + (y / 2), f'{y:.3f}', horizontalalignment="center", verticalalignment="center")
        y_sum += y
ax.grid()
ax.set_title("Area for each win/draw/lose rate per StopAt values in " + str(g1_runs) + " runs")
ax.set_xlabel("StopAt values")
ax.set_ylabel("Win/Draw/Lose rate")
ax.margins(0.025, 0)
ax.legend(["Win, beat croupier", "Win, croupier died", "Draw", "Lose, beat by croupier", "Lose, croupier also died"])
ax.set_xticks(STOP_AT_VALUES)
ax.set_yticks([x / 10.0 for x in range(0, 11)])

# Graph 2:
fig = plt.figure()
ax = fig.add_subplot(111)
for s_i, w in enumerate(g2_sum_win):
    ax.plot(CARDS, w, '-', linewidth=2, label=g2_strategies[s_i])
    for x, y in zip(CARDS, w):
        ax.text(x - 0.4 * s_i, y, f'{y:.3f}', color=TEXTCOLORS[s_i])
ax.grid()
ax.set_title("Win rate per initial card of the croupier for best strategies in " + str(g2_runs) + " runs")
ax.set_xlabel("Croupier's initial card")
ax.set_ylabel("Win rate")
ax.legend()

# Graph 3:
fig = plt.figure()
ax = fig.add_subplot(111)
for s_i, w in enumerate(g3_sum_win):
    ax.plot(STOP_AT_VALUES, w, '-', linewidth=2, label=STRATEGIES[s_i].__name__)
    for x, y in zip(STOP_AT_VALUES, w):
        ax.text(x - 0.4 * s_i, y, f'{y:.3f}', color=TEXTCOLORS[s_i])
ax.grid()
ax.set_title("Win/Draw rate per StopAt values for different strategies in " + str(g3_runs) + " runs")
ax.set_xlabel("StopAt values")
ax.set_ylabel("Win rate")
ax.legend()

plt.show()
