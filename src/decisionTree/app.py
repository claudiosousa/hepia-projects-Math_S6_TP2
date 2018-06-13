from pprint import pprint
from collections import defaultdict

# cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
# cards.sort()
cards = {i: 4 for i in range(2, 12)}
cards[10] = 16

stop_at = 16

def calc_points(picked):
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
    return res

def calculate(cards, picked, odds):

    res = {}
    res["total"] = defaultdict(int)
    res["local"] = defaultdict(int)
    tempcards = dict(cards)
    for card in cards.keys():
        newcards = dict(tempcards)
        newcards[card] -= 1
        if not newcards[card]:
            del newcards[card]

        card_count = tempcards[card]
        # del tempcards[card]

        newpicked = picked + [card]
        points = calc_points(newpicked)

        local_odds = card_count / (52 - len(picked))

        if points > stop_at:
            if points > 21:
                points = 0
            res["total"][points] += local_odds * odds
            res['local'][points] += local_odds
        else:
            child_odds = calculate(newcards, newpicked, local_odds)
            for child_card, child_odd in child_odds["total"].items():
                res["total"][child_card] += child_odd * odds
                res["local"][child_card] += child_odd

            if "children" not in res:
                res["children"] = {}
            res["children"][card] = child_odds

    return res


tree = calculate(cards, [], 1)
import json
print(json.dumps(tree))
