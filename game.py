from dice import Dice
from player import Player
import random


class Game:
    def __init__(self):
        self.no_of_dices = 5
        self.dices = [Dice(6) for _ in range(self.no_of_dices)]
        self.kept_dice_values = [None] * self.no_of_dices
        self.player = Player("You")
        self.bob = Player("Bob")

    def roll_dices(self, kept_dices):
        rolled_values = []
        for i in range(self.no_of_dices):
            if i in kept_dices:
                rolled_values.append(self.kept_dice_values[i])
            else:
                roll_value = self.dices[i].roll()
                self.kept_dice_values[i] = roll_value
                rolled_values.append(roll_value)
        print(f"Rolled dices: {rolled_values}")
        return rolled_values

    def keep_dice(self, index, keep=True):
        if keep:
            if self.kept_dice_values[index] is None:
                self.kept_dice_values[index] = self.dices[index].roll()
        else:
            self.kept_dice_values[index] = None

    def play_round(self, player):
        rolls_left = 2
        kept_dices = []

        while rolls_left > 0:
            response = input(
                "Enter your response ('roll' to roll, or dice numbers to keep): ") if player.name == "You" else 'roll'
            if response == 'roll':
                rolled_values = self.roll_dices(kept_dices)
                rolls_left -= 1
                print(f"Rolls left: {rolls_left}")

            possible_formations = player.suggest_formation(
                [v if isinstance(v, int) else int(
                    v.split('(')[1].split(')')[0]) for v in rolled_values]
            )

            if player.name == "You":
                self.handle_player_turn(
                    player, possible_formations, rolled_values)
            else:
                self.handle_bot_turn(
                    player, possible_formations, rolled_values)
                return

        self.handle_kept_dices(response)

    def handle_player_turn(self, player, possible_formations, rolled_values):
        if possible_formations:
            print(f"Suggested formations: {possible_formations}")
            accept = input(
                "Do you want to keep one of these formations? (Enter 1 if yes, or 'no' to continue rolling): ")
            if accept == '1':
                chosen_formation = input(
                    f"Choose formation from {possible_formations}: ")
                if chosen_formation in possible_formations:
                    player.keep_score(chosen_formation, rolled_values)
                    print(
                        f"Formation '{chosen_formation}' saved with dice {rolled_values}")
                else:
                    print("Invalid formation choice.")
        else:
            print("No valid formation suggestions.")

    def handle_bot_turn(self, player, possible_formations, rolled_values):
        chosen_formation = random.choice(possible_formations)
        player.keep_score(chosen_formation, rolled_values)
        print(
            f"Bob chose formation '{chosen_formation}' with dice {rolled_values}")

    def handle_kept_dices(self, response):
        try:
            kept_dices = list(map(int, response.split()))
            print(f"Kept dices: {kept_dices}")
        except ValueError:
            print(
                "Invalid input. Please enter dice numbers separated by space or 'roll' to roll the dices.")

    def start_game(self):
        print("Game started!")
        rounds = 13
        for round in range(1, rounds + 1):
            print(f"\n--- Round {round} ---")
            print("Your turn:")
            self.play_round(self.player)
            print("Bob's turn:")
            self.play_round(self.bob)

        self.display_final_scores()

    def display_final_scores(self):
        print("\nGame over! Final scores:")
        print(f"Your scores: {self.player.scores}")
        print(f"Bob's scores: {self.bob.scores}")
        print("Winner: You" if sum(self.player.scores.values())
              > sum(self.bob.scores.values()) else "Winner: Bob")
