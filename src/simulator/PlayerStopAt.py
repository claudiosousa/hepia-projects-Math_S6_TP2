#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simpliest player strategy: get at 16, keep at 17
# Author: Claudio Sousa, David Gonzalez
#

from deck import get_card_points

class PlayerStopAt:
    def __init__(self, stop_at):
        self.stop_at = stop_at

    def should_continue(self, cards, croupier_cards, others_cards):
        return get_card_points(cards) < self.stop_at

    def __str__(self):
        return PlayerStopAt.__name__ + "(" + str(self.stop_at) + ")"

    def __repr__(self):
        return self.__str__()
