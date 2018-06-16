from collections import defaultdict
from graphviz import Digraph
from pprint import pprint
from prettytable import PrettyTable

from deck import get_cards, calc_points


def plot_tree(tree):
    # dot = Digraph(engine="circo", format="pdf", body=['mindist=0.2', 'ratio=auto'])
    # dot = Digraph(engine="twopi", format="pdf", body=['ranksep=3', 'ratio=auto'])
    dot = Digraph(format="pdf", body=['mindist=0.2', 'ratio=auto'])

    def addNode(node, name):
        label = f'Card: {node["card"]}'
        label += f'\nSum: {node["sum"]}'
        outcome = node["outcome"]
        label += f'\nOdds: {outcome["win"]*100:>2.0f}/{outcome["draw"]*100:>2.0f}/{outcome["loose"]*100:>2.0f}'
        if "next_mode_odds" in node:
            label += f'\nLoose_next: {node["next_mode_odds"]:>2.0%}'

        dot.node(name, label)

        if "children" in node:
            for card, child in node['children'].items():
                child_name = f'{name}_{card}'
                addNode(child, child_name)
                dot.edge(name, child_name, f'{child["odds"]:>2.1%}')

    addNode(tree, '0')
    dot.render('output/player.gv', view=True)

def draw_interactive_odds(hands_odds):

    def calculate_for_croupier_initial_card(hand_odds):

        def calculate_outcome(sum):
            if sum == -1:
                return{
                    'win': 0,
                    'draw': 0,
                    'loose': 1
                }
            if sum < 17:
                sum = 16
            return hand_odds[sum - 16]

        tree = {
            'card': 'Initial state',
            'sum': '<=11',
            'cards': get_cards(),
            'picked': [],
            'outcome': calculate_outcome(0),
        }

        def calculate_next_level(node):

            cards = node['cards']
            picked = node['picked']

            node["children"] = {}

            tempcards = dict(cards)
            next_mode_odds = 0

            for card in cards.keys():
                newcards = dict(tempcards)
                newcards[card] -= 1
                if not newcards[card]:
                    del newcards[card]

                card_count = tempcards[card]
                newpicked = picked + [card]
                newpoints = calc_points(newpicked)

                odds = card_count / (52 - len(picked))
                outcome = calculate_outcome(newpoints)
                next_mode_odds += odds * (outcome['loose'])
                node["children"][card] = {
                    'card': card,
                    'odds': odds,
                    'sum': newpoints,
                    'outcome': outcome,
                    'cards': newcards,
                    'picked': newpicked
                }

            node["next_mode_odds"] = next_mode_odds
            return node["children"]

        children = calculate_next_level(tree)
        children = calculate_next_level(children[7])
        children = calculate_next_level(children[10])
        children = calculate_next_level(children[11])
        plot_tree(tree)

    return calculate_for_croupier_initial_card(hands_odds[9])
