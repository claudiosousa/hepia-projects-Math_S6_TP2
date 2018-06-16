from collections import defaultdict
from graphviz import Digraph
from pprint import pprint
from prettytable import PrettyTable

from deck import get_cards, calc_points

def player_hand_value_odds(croupier_odds):

    def get_lock(croupier):
        odds = [{
            'sum': '<=16',
            'win': float(croupier[-1]),
            'draw': 0.0,
            'loose': 1 - croupier[-1]
        }]
        for i in range(17, 22):
            win = croupier[-1]
            for j in range(17, i):
                win += croupier[j]

            draw = croupier[i]

            odds.append({
                'sum': i,
                'win': win,
                'draw': draw,
                'loose': 1 - win - draw
            })
        return odds

    res = {0: get_lock(croupier_odds['local'])}
    for i in range(2, 12):
        res[i] = get_lock(croupier_odds['children'][i]['local'])
    return res

def str_player_hand_value_odds(hand_odds):
    x = PrettyTable(["Hand", '-'] + list(map(str, range(2, 12))))

    res = [[0] * 12 for i in range(16, 22)]
    for card, hands in hand_odds.items():
        if card == 0:
            for i, hand in enumerate(hands):
                res[i][0] = hand['sum']

        for i, hand in enumerate(hands):
            if card == 0:
                card = 1

            res[i][card] = f"{hand['win']*100:>2.0f}/{hand['draw']*100:>2.0f}/{hand['loose']*100:>2.0f}"

    for row in res:
        x.add_row(row)

    return x.get_string(title="Player odds of winning")

def calculate_player_odds(hands_odds):

    def calculate_for_croupier_initial_card(hand_odds):

        tree = {
            'sum': '<=11',
            'outcome': hand_odds[0],
            'children': {}
        }

        def calculate(cards, picked, odds):

            points = calc_points(picked)
            meaningful = points == -1 or points > 11
            if meaningful:
                res = {}
                res["sum"] = points
                res["odds"] = odds
                if res['sum'] == -1:
                    res['outcome'] = {
                        'win': 0,
                        'draw': 0,
                        'loose': 1
                    }
                    res["children"] = {}
                    return res

                res['outcome'] =hand_odds[points-16]
                res["children"] = {}

            tempcards = dict(cards)
            for card in cards.keys():
                newcards = dict(tempcards)
                newcards[card] -= 1
                if not newcards[card]:
                    del newcards[card]

                card_count = tempcards[card]
                newpicked = picked + [card]

                local_odds = card_count / (52 - len(picked))

                child_odds = calculate(newcards, newpicked, local_odds)
                if child_odds:
                    if meaningful:
                        res["children"][card] = child_odds
                    else:
                        tree["children"][','.join(map(str, newpicked))] = child_odds
                del tempcards[card]

            return res if meaningful else None

        calculate(get_cards(), [], 1)
        return tree

    return calculate_for_croupier_initial_card(hands_odds[0])
