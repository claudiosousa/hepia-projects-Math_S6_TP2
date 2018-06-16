#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simulate a game with the given strategies
# Author: Claudio Sousa, David Gonzalez
#

from pprint import pprint
from deck import get_card_points, get_shuffled_deck

def playGame(croupier, players):
    deck = get_shuffled_deck()

    croupier_cards = []
    players_cards = [[] for _ in range(len(players))]

    # initial draw
    for i, p in enumerate(players):
        players_cards[i].append(deck.pop())
        players_cards[i].append(deck.pop())

    croupier_cards.append(deck.pop())

    # play the game
    for i, p in enumerate(players):
        player_cards = players_cards[i]
        others_cards = [cards for cards in players_cards if cards is not player_cards]
        while get_card_points(player_cards)>=0 and p.should_continue(player_cards, croupier_cards, others_cards):
            player_cards.append(deck.pop())

    while get_card_points(croupier_cards)>=0 and croupier.should_continue(croupier_cards, croupier_cards, players_cards):
        croupier_cards.append(deck.pop())

    # check wins
    croupier_wins = 0
    player_wins = [0] * len(players)
    player_died = [0] * len(players)

    croupier_points = get_card_points(croupier_cards)
    for i, player_cards in enumerate(players_cards):
        player_points = get_card_points(player_cards)

        if player_points < 0: # player dies, lose everytime
            player_wins[i] -= 1
            croupier_wins += 1
            player_died[i] = 1
        else: # player doesn't die
            if croupier_points < 0: # croupier dies, player wins
                player_wins[i] += 1
                croupier_wins -= 1
                player_died[i] = 1
            else: # croupier doesn't die
                if croupier_points == player_points: # draw
                    pass
                else:
                    res = 1 if player_points > croupier_points else -1 # player wins
                    player_wins[i] += res
                    croupier_wins -= res

    # pprint(sum(croupier_cards))
    # pprint([sum(a) for a in players_cards])
    return croupier_wins, player_wins, player_died, croupier_cards
