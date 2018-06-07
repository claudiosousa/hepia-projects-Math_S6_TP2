from random import shuffle

def get_shuffled_deck():
    cartes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    shuffle(cartes)
    return cartes



def get_card_points(cards):
    """
    -1: exploded!
    0-21: the points
    22: 21 points AND it is ACE + figure
    """

    # TODO:
    #  Needed to distinguishe figures from10
    # handle ACES

    points = sum(cards)
    if points >= 22:
        points = -1

    return points