#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KO count strategies:
#   https://www.blackjacktactics.com/blackjack/strategy/card-counting/ko/
# Author: Claudio Sousa, David Gonzalez
#

from deck import get_card_points

class PlayerKOCount:
    def __init__(self, stop_at):
        self.stop_at = stop_at

    def should_continue(self, cards, croupier_cards, others_cards):
        count = 0
        all_played_cards = cards + croupier_cards
        for oc in others_cards:
            all_played_cards += oc

        for c in all_played_cards:
            if c < 7:
                count += 1
            elif c > 9:
                count -= 1

        return get_card_points(cards) < min(self.stop_at - count / 4, 21)

    def __str__(self):
        return PlayerKOCount.__name__ + "(" + str(self.stop_at) + ")"

    def __repr__(self):
        return self.__str__()
