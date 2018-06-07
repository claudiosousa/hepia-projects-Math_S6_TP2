from pprint import pprint

from PlayerStopAt import PlayerStopAt
from simulator import playGame

PLAYERS = 7

croupier = PlayerStopAt(17)
players = [PlayerStopAt(17) for _ in range(PLAYERS)]

result = playGame(croupier, players)
pprint(result)
