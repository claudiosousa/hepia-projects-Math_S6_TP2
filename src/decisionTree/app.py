from collections import defaultdict
from pprint import pprint
import json

from croupier import calculate_croupier_odds, build_croupier_graph
from player import player_hand_value_odds, calculate_player_odds, str_player_hand_value_odds

croupier_odds = calculate_croupier_odds()
# print(json.dumps(croupier_odds))

dot = build_croupier_graph(croupier_odds)
#dot.render('output/croupier.gv', view=True)

# print(dot.source)

hand_odds = player_hand_value_odds(croupier_odds)
#print(str_player_hand_value_odds(hand_odds))

player_odds = calculate_player_odds(hand_odds)
#print(json.dumps(player_odds))

exit()


first_level = {'children': {}}

for cards, child in player_odds['children'].items():
    first_level['children'][cards]= child


for cards, child in first_level.items():
    first_level[cards] = sorted(first_level[cards])
pprint(first_level)
exit()
