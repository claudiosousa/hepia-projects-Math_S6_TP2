from deck import get_card_points

class PlayerStopAt:
    def __init__(self, stop_at):
        self.stop_at = stop_at

    def should_continue(self, cards, croupier_cards, others_cards):
        points = get_card_points(cards)
        return points < self.stop_at and points >=0 # points < 0 => over 21