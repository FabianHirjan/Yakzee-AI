from player import Player


class YahtzeeGame:
    def __init__(self):
        self.player = Player("You")
        self.bob = Player("Bob")

    def roll_bob_dice(self):
        """Roll the dice for Bob."""
        self.bob.roll_dice()

    def get_player_dice_values(self):
        """Get the player's dice values."""
        return self.player.get_dice_values()

    def get_bob_dice_values(self):
        """Get Bob's dice values."""
        return self.bob.get_dice_values()

    def get_scores(self, player):
        """Get the initial scores for the given player."""
        return {
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
            "Chance": 0
        }
