#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create a nice graph for hand_odds.csv
# Author: Claudio Sousa, David Gonzalez
#

from pprint import pprint
import csv
import matplotlib.pyplot as plt

colors =  [(0.3, 1.0, 0.3), (0.6, 0.6, 0.6), (1.0, 0.3, 0.3)]
cards = []
points = []
rates = []

with open('hand_odds.csv', 'r') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        idx = int(row[0])
        if idx > 0:
            idx -= 1

        if idx == len(rates):
            cards.append(int(row[0]))
            rates.append([])

        p = int(row[1])
        if p not in points:
            points.append(p)

        rates[idx].append(float(row[2]) / 100)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.stackplot(range(len(cards)), list(map(list, zip(*rates))), colors=colors)
ax.plot(range(len(cards)), [range(len(points) + 1) for _ in range(len(cards))], '-', linewidth=1, c="black")
for x, w in zip(range(len(cards) + 1), rates):
    y_sum = 0
    for y in w:
        if y > 0.1:
            ax.text(x, y_sum + (y / 2), f'{y:.2f}', horizontalalignment="center", verticalalignment="center")
        y_sum += y
ax.grid()
ax.set_title("Area for each win/draw/lose rate per croupier's initial card and final point")
ax.set_xlabel("Croupier's initial card")
ax.set_ylabel("Win/Draw/Lose rate per final point")
ax.margins(0.025, 0)

plt.sca(ax)
plt.xticks(range(len(cards)), cards)
plt.yticks(range(len(points)), points)

plt.show()
