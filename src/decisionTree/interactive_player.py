from collections import defaultdict
from graphviz import Digraph
from pprint import pprint
from prettytable import PrettyTable

from deck import get_cards, calc_points
from croupier import calculate_croupier_odds
from player import player_hand_value_odds


def plot_tree(tree):
    # dot = Digraph(engine="circo", format="pdf", body=['mindist=0.2', 'ratio=auto'])
    # dot = Digraph(engine="twopi", format="pdf", body=['ranksep=3', 'ratio=auto'])
    dot = Digraph(format="pdf", body=['mindist=0.2', 'ratio=auto'])

    def addNode(node, name):

        label = str(node["card"])
        if node['sum'] != 0:
            label='Card: ' + label
        label += f'\nSum: {node["sum"]}'
        outcome=node["outcome"]
        label += f'\nWin: {outcome["win"]*100:>2.0f}'
        label += f'\nDraw: {outcome["draw"]*100:>2.0f}'
        label += f'\nLoose: {outcome["loose"]*100:>2.0f}'
        if "next_mode_odds" in node:
            label += f'\nNext_loose: {node["next_mode_odds"]:>2.0%}'

        color='white'
        if "mode" in node:
            mode=node['mode']
            if mode == 'next':
                color="gray85"
            elif node["next_mode_odds"] - outcome["loose"] > 0.01:
                color="brown1"
            else:
                color="limegreen"

        dot.node(name, label, fillcolor=color, style="filled")

        if "children" in node:
            for card, child in node['children'].items():
                child_name=f'{name}_{card}'
                addNode(child, child_name)
                dot.edge(name, child_name, f'{child["odds"]:>2.1%}')

    addNode(tree, '0')
    dot.render('output/player.gv', view=True)

def draw_interactive_odds(hands_odds):

    def calculate_for_croupier_initial_card(hand_odds, card_croupier):

        def calculate_outcome(sum):
            if sum == -1:
                return{
                    'win': 0,
                    'draw': 0,
                    'loose': 1
                }
            if sum < 17:
                sum=16
            return hand_odds[sum - 16]

        tree={
            'card': f'Croupier {card_croupier}',
            'sum': '0',
            'cards': get_cards(),
            'picked': [],
            'outcome': calculate_outcome(0),
        }

        def calculate_next_level(node):

            cards=node['cards']
            picked=node['picked']
            current['mode']="current"
            node["children"]={}

            tempcards=dict(cards)
            next_mode_odds=0

            for card in cards.keys():
                newcards=dict(tempcards)
                newcards[card] -= 1
                if not newcards[card]:
                    del newcards[card]

                card_count=tempcards[card]
                newpicked=picked + [card]
                newpoints=calc_points(newpicked)

                odds=card_count / (52 - len(picked))
                outcome=calculate_outcome(newpoints)
                next_mode_odds += odds * (outcome['loose'])
                node["children"][card]={
                    'card': card,
                    'odds': odds,
                    'sum': newpoints,
                    'outcome': outcome,
                    'cards': newcards,
                    'picked': newpicked,
                    'mode': "next"
                }

            node["next_mode_odds"]=next_mode_odds
            return node["children"]

        current=tree
        children=calculate_next_level(tree)
        plot_tree(tree)
        while True:
            plot_tree(tree)
            card=int(input("Card picked: "))
            del current['mode']
            for _, child in children.items():
                del child['mode']
            current=children[card]
            children=calculate_next_level(current)

    card=int(input("Croupier's card: "))
    return calculate_for_croupier_initial_card(hands_odds[card], card)


if __name__ == "__main__":
    croupier_odds=calculate_croupier_odds()
    hand_odds=player_hand_value_odds(croupier_odds)
    draw_interactive_odds(hand_odds)
