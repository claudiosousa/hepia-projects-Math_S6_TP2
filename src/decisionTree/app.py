from pprint import pprint

from croupier import calculate_croupier_odds, build_graph

croupier_odds = calculate_croupier_odds()
dot = build_graph(croupier_odds)

dot.render('output/croupier.gv', view=True)
print(dot.source)
