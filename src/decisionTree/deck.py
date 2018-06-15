def get_cards():
    cards = {i: 4 for i in range(2, 12)}
    cards[10] = 16
    return cards

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
