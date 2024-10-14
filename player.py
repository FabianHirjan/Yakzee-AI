from collections import Counter


class Player:
    def __init__(self, name):
        self.name = name
        self.scores = {}  # Un dicționar pentru a păstra scorul pe diverse combinații

    def suggest_formation(self, rolled_values):
        counts = Counter(rolled_values)
        counts_values = list(counts.values())
        possible_formations = []

        # Adăugăm perechile ones, twos etc.

        # Verificăm diverse formații avansate
        if 5 in counts_values:
            possible_formations.append("Yahtzee!")
        elif 4 in counts_values:
            possible_formations.append("Four of a Kind")
        elif 3 in counts_values and 2 in counts_values:
            possible_formations.append("Full House")
        elif 3 in counts_values:
            possible_formations.append("Three of a Kind")
        elif sorted(rolled_values) in [list(range(1, 6)), list(range(2, 7))]:
            possible_formations.append("Large Straight")
        elif set([1, 2, 3, 4]) <= set(rolled_values) or set([2, 3, 4, 5]) <= set(rolled_values) or set([3, 4, 5, 6]) <= set(rolled_values):
            possible_formations.append("Small Straight")
        elif 2 in counts_values:
            if counts_values.count(2) == 2:
                possible_formations.append("Two Pairs")
            else:
                possible_formations.append("One Pair")

        return possible_formations
