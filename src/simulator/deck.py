#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Deck utility functions
# Author: Claudio Sousa, David Gonzalez
#

from random import shuffle

def get_shuffled_deck():
    cartes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    shuffle(cartes)
    return cartes

def get_card_points(picked):
    """
    -1: exploded!
    0-21: the points
    22: 21 points AND it is ACE + figure
    """
    res = 0
    ace = False
    for i in picked:
        if i == 11:
            if ace:
                i = 1
            else:
                ace = True
        res += i

    if res > 21 and ace:
        res -= 10

    if res > 21:
        res = -1

    if res == 21 and len(picked) == 2:  # blackjack
        res = 22

    return res

def get_card_points_old(cards):
    """
    -1: exploded!
    0-21: the points
    22: 21 points AND it is ACE + figure
    """

    points = sum(cards)
    if points > 21:
        cards = [c if c != 11 else 1 for c in cards]
        if points > 21:
            return -1

    if points == 21 and len(cards) == 2:  # blackjack
        points = 22

    return points
