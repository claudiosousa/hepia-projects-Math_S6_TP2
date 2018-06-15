from collections import defaultdict
from graphviz import Digraph

from deck import get_cards, calc_points

def calculate_croupier_odds():
    stop_at = 16
    def calculate(cards, picked, odds):

        res = {}
        res["odds"] = odds
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

    return calculate(get_cards(), [], 1)


def build_graph(croupier_odds):
    dot = Digraph(engine="circo", format="pdf", body=['mindist=0.2', 'ratio=auto'])
    #dot = Digraph(engine="twopi", format="pdf", body=['ranksep=3', 'ratio=auto'])
    def addNode(node, name, label, level):
        items = list(node['local'].items())
        items.sort()
        for res, odds in items:
            if res == 0:
                res = '-'
            label += f'\n{res}: {odds:>2.0%}'
        dot.node(name, label)

        if level >= 1:
            return
        if "children" in node:
            for card, child in node['children'].items():
                child_name = f'{name}_{card}'
                addNode(child, child_name, f'Card: {card}', level + 1)
                dot.edge(name, child_name, f'{child["odds"]:>2.1%}')


    addNode(croupier_odds, '0', 'Initial state', 0)
    return dot