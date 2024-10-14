import tkinter as tk
from tkinter import messagebox, simpledialog
from dice import Dice
from player import Player
import random


class YahtzeeGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahtzee Game")

        self.no_of_dices = 5
        self.dices = [Dice(6) for _ in range(self.no_of_dices)]
        self.kept_dice_values = [None] * self.no_of_dices
        self.kept_dices = []

        self.player = Player("You")
        self.bob = Player("Bob")

        self.rolls_left = 3

        self.dice_labels = []
        self.dice_buttons = []
        self.create_widgets()
        self.update_dice_display()

    def create_widgets(self):
        tk.Label(self.root, text="Your Dice:").grid(
            row=0, column=0, columnspan=5)

        for i in range(self.no_of_dices):
            dice_label = tk.Label(self.root, text="0", font=("Helvetica", 20))
            dice_label.grid(row=1, column=i)
            self.dice_labels.append(dice_label)

            dice_button = tk.Button(
                self.root, text="Keep", command=lambda i=i: self.toggle_keep_dice(i))
            dice_button.grid(row=2, column=i)
            self.dice_buttons.append(dice_button)

        self.roll_button = tk.Button(
            self.root, text="Roll", command=self.roll_dices)
        self.roll_button.grid(row=3, column=0, columnspan=5)

        self.formations_label = tk.Label(
            self.root, text="Formations: None", font=("Helvetica", 14))
        self.formations_label.grid(row=4, column=0, columnspan=5)

        self.scores_label = tk.Label(
            self.root, text="Your Score: 0\nBob's Score: 0", font=("Helvetica", 14))
        self.scores_label.grid(row=5, column=0, columnspan=5)

        self.player_formations_frame = tk.Frame(self.root)
        self.player_formations_frame.grid(row=6, column=0, columnspan=5)

        self.update_formations_display()

    def roll_dices(self):
        if self.rolls_left > 0:
            rolled_values = []
            for i in range(self.no_of_dices):
                if i not in self.kept_dices:
                    roll_value = self.dices[i].roll()
                    self.kept_dice_values[i] = roll_value
                rolled_values.append(self.kept_dice_values[i])

            self.update_dice_display()
            self.rolls_left -= 1
            possible_formations = self.player.suggest_formation(rolled_values)

            if possible_formations:
                self.formations_label.config(
                    text=f"Formations: {', '.join(possible_formations)}")
            else:
                self.formations_label.config(text="Formations: None")

            if self.rolls_left == 0:
                self.choose_formation(possible_formations)

    def update_dice_display(self):
        for i, dice_value in enumerate(self.kept_dice_values):
            self.dice_labels[i].config(
                text=str(dice_value) if dice_value else "0")

    def toggle_keep_dice(self, dice_index):
        if dice_index in self.kept_dices:
            self.kept_dices.remove(dice_index)
            self.dice_buttons[dice_index].config(text="Keep")
        else:
            self.kept_dices.append(dice_index)
            self.dice_buttons[dice_index].config(text="Unkeep")

    def choose_formation(self, possible_formations):
        if not possible_formations:
            messagebox.showinfo(
                "No Formation", "No valid formation available!")
            return

        chosen_formation = simpledialog.askstring(
            "Choose Formation", f"Possible formations: {', '.join(possible_formations)}")

        if chosen_formation and chosen_formation in possible_formations:
            # Calculate the score based on kept dice values
            # Modify this line if scoring logic is different
            score = sum(self.kept_dice_values)
            self.player.scores[chosen_formation] = score
            self.update_formations_display()
            messagebox.showinfo("Formation Chosen",
                                f"You chose: {chosen_formation}")
            self.end_turn()
        else:
            messagebox.showinfo("Invalid Selection",
                                "Invalid formation chosen!")

    def update_formations_display(self):
        for widget in self.player_formations_frame.winfo_children():
            widget.destroy()

        for formation in range(1, 7):
            score = self.player.scores.get(f"{formation}s", 0)
            tk.Label(self.player_formations_frame,
                     text=f"{formation}s: {score}").pack(anchor='w')

        advanced_formations = ["Yahtzee!", "Four of a Kind", "Full House",
                               "Three of a Kind", "Large Straight", "Small Straight", "Two Pairs", "One Pair"]
        for formation in advanced_formations:
            score = self.player.scores.get(formation, 0)
            tk.Label(self.player_formations_frame,
                     text=f"{formation}: {score}").pack(anchor='w')

    def end_turn(self):
        # Reset for a new turn
        self.rolls_left = 3
        self.kept_dice_values = [None] * self.no_of_dices
        self.kept_dices = []
        self.update_dice_display()
        self.bob_turn()

    def bob_turn(self):
        # Bob makes random moves
        rolled_values = [random.randint(1, 6) for _ in range(self.no_of_dices)]
        possible_formations = self.bob.suggest_formation(rolled_values)

        if possible_formations:
            chosen_formation = random.choice(possible_formations)
            score = sum(rolled_values)  # Calculate the score for Bob
            self.bob.scores[chosen_formation] = score

            # Update the scores label
            self.scores_label.config(
                text=f"Your Score: {sum(self.player.scores.values())}\nBob's Score: {sum(self.bob.scores.values())}")
            messagebox.showinfo(
                "Bob's Turn", f"Bob chose formation: {chosen_formation}")

        self.rolls_left = 3


if __name__ == "__main__":
    root = tk.Tk()
    game = YahtzeeGameGUI(root)
    root.mainloop()
