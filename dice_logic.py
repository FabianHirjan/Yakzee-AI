def one_pair(dices):
    dices_values = sorted([dice.value for dice in dices])
    for i in range(4, 0, -1):
        if dices_values[i] == dices_values[i-1]:
            return sum(dices_values)
    return 0


def two_pairs(dices):
    dices_values = sorted([dice.value for dice in dices])
    pairs = 0
    score = 0
    for i in range(4, 0, -1):
        if dices_values[i] == dices_values[i-1]:
            pairs += 1
            score += dices_values[i]
            if pairs == 2:
                return score
    return 0


def three_of_a_kind(dices):
    dices_values = sorted([dice.value for dice in dices])
    for i in range(4, 1, -1):
        if dices_values[i] == dices_values[i-1] == dices_values[i-2]:
            return sum(dices_values)
    return 0


def four_of_a_kind(dices):
    dices_values = sorted([dice.value for dice in dices])
    for i in range(4, 2, -1):
        if dices_values[i] == dices_values[i-1] == dices_values[i-2] == dices_values[i-3]:
            return sum(dices_values)
    return 0


def full_house(dices):
    dices_values = sorted([dice.value for dice in dices])
    if dices_values[0] == dices_values[1] and dices_values[2] == dices_values[4]:
        return 25
    if dices_values[0] == dices_values[2] and dices_values[3] == dices_values[4]:
        return 25
    return 0


def small_straight(dices):
    dices_values = sorted([dice.value for dice in dices])
    if dices_values == [1, 2, 3, 4, 5] or dices_values == [2, 3, 4, 5, 6]:
        return 30
    return 0


def large_straight(dices):
    dices_values = sorted([dice.value for dice in dices])
    if dices_values == [1, 2, 3, 4, 5] or dices_values == [2, 3, 4, 5, 6]:
        return 40
    return 0


def yahtzee(dices):
    dices_values = sorted([dice.value for dice in dices])
    if dices_values[0] == dices_values[4]:
        return 50
    return 0


def chance(dices):
    return sum([dice.value for dice in dices])


formations = ["One Pair", "Two Pairs", "Three of a Kind", "Four of a Kind",
              "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance"]


def formations_check(dices, formation):
    if formation == "One Pair":
        return one_pair(dices)
    elif formation == "Two Pairs":
        return two_pairs(dices)
    elif formation == "Three of a Kind":
        return three_of_a_kind(dices)
    elif formation == "Four of a Kind":
        return four_of_a_kind(dices)
    elif formation == "Full House":
        return full_house(dices)
    elif formation == "Small Straight":
        return small_straight(dices)
    elif formation == "Large Straight":
        return large_straight(dices)
    elif formation == "Yahtzee":
        return yahtzee(dices)
    elif formation == "Chance":
        return chance(dices)
    return 0
