from deck import get_card_points

class PlayerStopAt17:

    def should_continue(self, cards, croupier_cards, others_cards):
        points = get_card_points(cards)
        return points <= 16 and points >=0 # points < 0 => over 21