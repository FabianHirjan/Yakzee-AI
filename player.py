from collections import Counter

class Player:
    def __init__(self, name):
        self.name = name
        self.scores = {}

    def suggest_formation(self, rolled_values):
        counts = Counter(rolled_values)
        counts_values = list(counts.values())
        possible_formations = []

        if 5 in counts_values:
            possible_formations.append("Yahtzee!")
        elif 4 in counts_values:
            possible_formations.append("Four of a Kind")
        elif 3 in counts_values and 2 in counts_values:
            possible_formations.append("Full House")
        elif 3 in counts_values:
            possible_formations.append("Three of a Kind")
        if sorted(rolled_values) == [1, 2, 3, 4, 5] or sorted(rolled_values) == [2, 3, 4, 5, 6]:
            possible_formations.append("Large Straight")

        elif set([1, 2, 3, 4]).issubset(rolled_values) or set([2, 3, 4, 5]).issubset(rolled_values) or set([3, 4, 5, 6]).issubset(rolled_values):
            possible_formations.append("Small Straight")
 
        if counts_values.count(2) == 2:
            possible_formations.append("Two Pairs")
        elif 2 in counts_values:
            possible_formations.append("One Pair")

        return possible_formations

   