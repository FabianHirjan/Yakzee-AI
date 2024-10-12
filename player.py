from dice import Dice


class Player:
    def __init__(self, name):
        self.name = name
        self.dice = [Dice() for _ in range(5)]
        self.selected_dice = [False] * 5

    def roll_dice(self):
        """Roll the dice that are not selected."""
        for i, die in enumerate(self.dice):
            if not self.selected_dice[i]:
                die.roll()

    def get_dice_values(self):
        """Get the current values of the dice."""
        return [die.get_value() for die in self.dice]

    def toggle_dice_selection(self, index):
        """Toggle the selection of a dice."""
        self.selected_dice[index] = not self.selected_dice[index]
