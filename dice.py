import random


class Dice:
    def __init__(self):
        self.value = 1

    def roll(self):
        """Roll the dice to get a new value."""
        self.value = random.randint(1, 6)

    def get_value(self):
        """Return the current value of the dice."""
        return self.value
