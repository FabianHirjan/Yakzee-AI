import tkinter as tk
from tkinter import ttk
from yahtzee import YahtzeeGame


class YahtzeeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yahtzee")
        self.root.geometry("1800x1600")
        self.root.configure(bg="#212121")  # Dark background

        self.game = YahtzeeGame()

        # Stylish fonts and color scheme
        self.title_style = {"font": ("Roboto", 48, "bold"),
                            "bg": "#212121", "fg": "#FFD700"}
        self.label_style = {"font": ("Roboto", 24),
                            "bg": "#303030", "fg": "white"}
        self.button_style = {"font": ("Roboto", 20), "bg": "#007bff", "fg": "white",
                             "activebackground": "#0056b3", "relief": "flat", "borderwidth": 0}
        self.entry_style = {"font": ("Roboto", 20),
                            "bg": "#424242", "fg": "white", "justify": "center"}

        # Title with more visual prominence
        self.title_label = tk.Label(
            self.root, text="Yahtzee", **self.title_style)
        self.title_label.pack(pady=20)

        # Separate frames for player and Bob's dice with spacing
        self.player_dice_frame = tk.Frame(self.root, bg="#212121")
        self.player_dice_frame.pack(pady=20)

        self.bob_dice_frame = tk.Frame(self.root, bg="#212121")
        self.bob_dice_frame.pack(pady=20)

        self.dice_buttons, self.dice_labels = self.create_dice_widgets(
            self.player_dice_frame, row_offset=0, button_command=self.toggle_dice_selection)
        self.bob_dice_labels = self.create_dice_widgets(
            self.bob_dice_frame, row_offset=0, button_state=tk.DISABLED)[1]

        # Centered button with modern styling
        self.play_button_frame = tk.Frame(self.root, bg="#212121")
        self.play_button_frame.pack(pady=20)

        self.play_button = tk.Button(
            self.play_button_frame, text="Roll Dice", **self.button_style, command=self.play)
        self.play_button.pack()

        # Score frame with improved layout
        self.score_frame = tk.Frame(self.root, bg="#212121")
        self.score_frame.pack(pady=20, padx=20)

        self.create_score_frame()

        self.root.mainloop()

    def create_dice_widgets(self, parent_frame, row_offset=0, button_command=None, button_state=tk.NORMAL):
        buttons = []
        labels = []
        for i in range(5):
            button = tk.Button(parent_frame, text=f"{i + 1}", **self.button_style,
                               width=4, command=lambda i=i: button_command(
                                   i) if button_command else None,
                               state=button_state)
            button.grid(row=row_offset, column=i,
                        padx=10, pady=10)
            buttons.append(button)

            label = tk.Label(parent_frame, text="1",
                             **self.label_style, width=4)
            label.grid(row=row_offset + 1, column=i,
                       padx=10, pady=10)
            labels.append(label)
        return buttons, labels

    def create_score_frame(self):
        self.score_labels = self.create_score_widgets("Your Scores", 0)
        self.bob_score_labels = self.create_score_widgets("Bob's Scores", 2)

        self.player_score_label = tk.Label(
            self.score_frame, text="Score: 0", **self.label_style)
        self.player_score_label.grid(
            row=len(self.game.get_player_scores()) + 2, column=0, pady=10)

        self.bob_score_label = tk.Label(
            self.score_frame, text="Score: 0", **self.label_style)
        self.bob_score_label.grid(
            row=len(self.game.get_bob_scores()) + 2, column=2, pady=10)

    def create_score_widgets(self, text, col_offset):
        tk.Label(self.score_frame, text=text, **
                 self.label_style).grid(row=0, column=col_offset, padx=20, pady=10)

        score_entries = {}
        for i, score_name in enumerate(self.game.get_player_scores().keys()):
            tk.Label(self.score_frame, text=score_name, **
                     self.label_style).grid(row=i + 1, column=col_offset, padx=20, pady=5)
            score_entry = tk.Entry(
                self.score_frame, **self.entry_style, width=6)
            score_entry.grid(row=i + 1, column=col_offset + 1, padx=20)
            score_entries[score_name] = score_entry

        return score_entries

    def play(self):
        self.game.player.roll_dice()
        self.update_dice_labels(
            self.dice_labels, self.game.get_player_dice_values())

        self.game.roll_bob_dice()
        self.update_dice_labels(self.bob_dice_labels,
                                self.game.get_bob_dice_values())

        self.update_scores()

    def update_dice_labels(self, labels, values):
        for label, value in zip(labels, values):
            label.config(text=str(value))

    def update_scores(self):
        self.player_score_label.config(
            text="Score: " + str(sum(self.game.get_player_dice_values())))
        self.bob_score_label.config(
            text="Score: " + str(sum(self.game.get_bob_dice_values())))

    def toggle_dice_selection(self, index):
        self.game.player.toggle_dice_selection(index)
        if self.game.player.selected_dice[index]:
            self.dice_buttons[index].config(bg="#9400D3")  # Purple
        else:
            self.dice_buttons[index].config(bg="#007bff")  # Blue
