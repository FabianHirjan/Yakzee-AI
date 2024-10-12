import random


class Dice:
    def __init__(self):
        self.value = 1

    def roll(self):
        self.value = random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name
        self.dice = [Dice() for _ in range(5)]
        self.selected_dice = [False] * 5

    def roll_dice(self):
        for i, die in enumerate(self.dice):
            if not self.selected_dice[i]:  # throw only unselected dices
                die.roll()

    def get_dice_values(self):
        return [die.value for die in self.dice]

    def toggle_dice_selection(self, index):
        self.selected_dice[index] = not self.selected_dice[index]


class YahtzeeGame:
    def __init__(self):
        self.player = Player("You")
        self.bob = Player("Bob")

    def roll_bob_dice(self):
        self.bob.roll_dice()

    def get_player_dice_values(self):
        return self.player.get_dice_values()

    def get_bob_dice_values(self):
        return self.bob.get_dice_values()

    def get_player_scores(self):
        # Actualizăm numele scorurilor pentru jucător
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

    def get_bob_scores(self):
        # Actualizăm numele scorurilor pentru Bob
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
