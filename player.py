# player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.scores = {}
        self.formations = {
            "Ones": 0,
            "Twos": 0,
            "Threes": 0,
            "Fours": 0,
            "Fives": 0,
            "Sixes": 0,
            "Three of a Kind": 0,
            "Four of a Kind": 0,
            "Full House": 0,
            "Small Straight": 0,
            "Large Straight": 0,
            "Yahtzee": 0,
            "Chance": 0,
            "Two Pairs": 0
        }

    def suggest_formation(self, rolled_values):
        suggestions = []
        if rolled_values.count(2) >= 2:
            suggestions.append(("Two Pairs", self.formations["Two Pairs"]))
        return suggestions

    def keep_score(self, formation, dice_values):
        self.scores[formation] = sum(dice_values)
