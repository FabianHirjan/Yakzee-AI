import tkinter as tk
from yahtzee import YahtzeeGame


class YahtzeeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yahtzee")
        self.game = YahtzeeGame()

        # Player frame
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(side=tk.TOP, fill=tk.X)

        # Playber labe
        self.player_label = tk.Label(
            self.player_frame, text="Player: You", font=("Arial", 24))
        self.player_label.pack()

        # Dices and play button frame
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Play button
        self.play_button = tk.Button(
            self.bottom_frame, text="Roll Dice", font=("Arial", 18), command=self.play)
        self.play_button.pack(pady=10)

        # Dices
        self.dice_labels = []
        self.dice_buttons = []
        for i in range(5):
            button = tk.Button(self.bottom_frame, text="Die " + str(i + 1), font=(
                "Arial", 18), width=5, command=lambda i=i: self.toggle_dice_selection(i))
            button.pack(side=tk.LEFT, padx=5)
            self.dice_buttons.append(button)
            self.dice_labels.append(
                tk.Label(self.bottom_frame, text="1", font=("Arial", 18), width=5))
            self.dice_labels[-1].pack(side=tk.LEFT, padx=5)

        # Bob's dices
        self.bob_frame = tk.Frame(self.root)
        self.bob_frame.pack(side=tk.TOP, fill=tk.X)

        # Bob label
        self.bob_label = tk.Label(
            self.bob_frame, text="Player: Bob", font=("Arial", 24))
        self.bob_label.pack()

        # Bob dices
        self.bob_dice_labels = []
        self.bob_dice_buttons = []
        for i in range(5):
            button = tk.Button(self.bob_frame, text="Bob's Die " + str(i + 1), font=(
                "Arial", 18), width=5, command=lambda i=i: self.toggle_bob_dice_selection(i))
            button.pack(side=tk.LEFT, padx=5)
            self.bob_dice_buttons.append(button)
            self.bob_dice_labels.append(
                tk.Label(self.bob_frame, text="1", font=("Arial", 18), width=5))
            self.bob_dice_labels[-1].pack(side=tk.LEFT, padx=5)

        # Scores table frame
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        # Scores
        self.score_labels = {}
        for score_name in self.game.get_player_scores().keys():
            label = tk.Label(self.score_frame,
                             text=score_name, font=("Arial", 16))
            label.pack(anchor=tk.W)
            score_entry = tk.Entry(
                self.score_frame, font=("Arial", 16), width=5)
            score_entry.pack(anchor=tk.W)
            self.score_labels[score_name] = score_entry

        # Bob scores
        self.bob_score_labels = {}
        for score_name in self.game.get_bob_scores().keys():
            label = tk.Label(self.score_frame, text=score_name +
                             " (Bob)", font=("Arial", 16))
            label.pack(anchor=tk.W)
            score_entry = tk.Entry(
                self.score_frame, font=("Arial", 16), width=5)
            score_entry.pack(anchor=tk.W)
            self.bob_score_labels[score_name] = score_entry

        # points label
        self.player_score_label = tk.Label(
            self.player_frame, text="Score: 0", font=("Arial", 18))
        self.player_score_label.pack()

        self.bob_score_label = tk.Label(
            self.bob_frame, text="Score: 0", font=("Arial", 18))
        self.bob_score_label.pack()

        self.root.mainloop()

    def play(self):
        # Player's throw
        self.game.player.roll_dice()
        for i, label in enumerate(self.dice_labels):
            label.config(text=str(self.game.get_player_dice_values()[i]))

        # Bob's throw
        self.game.roll_bob_dice()
        for i, label in enumerate(self.bob_dice_labels):
            label.config(text=str(self.game.get_bob_dice_values()[i]))

        # Scores TODO
        self.update_scores()

    def update_scores(self):
        # TODO
        self.player_score_label.config(
            text="Score: " + str(sum(self.game.get_player_dice_values())))
        self.bob_score_label.config(
            text="Score: " + str(sum(self.game.get_bob_dice_values())))

    def toggle_dice_selection(self, index):
        self.game.player.toggle_dice_selection(index)
        if self.game.player.selected_dice[index]:
            self.dice_buttons[index].config(relief=tk.SUNKEN, bg='yellow')
        else:
            self.dice_buttons[index].config(relief=tk.RAISED, bg='lightgrey')

    def toggle_bob_dice_selection(self, index):
        self.game.bob.toggle_dice_selection(index)
        if self.game.bob.selected_dice[index]:
            self.bob_dice_buttons[index].config(relief=tk.SUNKEN, bg='yellow')
        else:
            self.bob_dice_buttons[index].config(
                relief=tk.RAISED, bg='lightgrey')
