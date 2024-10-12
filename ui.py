import tkinter as tk
from tkinter import messagebox
from yahtzee import YahtzeeGame


class YahtzeeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yahtzee")
        self.root.geometry("2000x1800")
        self.root.configure(bg="#212121")

        self.game = YahtzeeGame()
        self.rolls_left = 2

        self.init_styles()
        self.create_widgets()

        self.root.mainloop()

    def init_styles(self):
        self.title_style = {
            "font": ("Roboto", 12, "bold"), "bg": "#212121", "fg": "#FFD700"}
        self.label_style = {
            "font": ("Roboto", 12), "bg": "#303030", "fg": "#FFD700"}
        self.button_style = {
            "font": ("Roboto", 12),
            "bg": "#007bff",
            "fg": "black",
            "activebackground": "#0056b3",
            "relief": "flat",
            "borderwidth": 0,
        }
        self.entry_style = {
            "font": ("Roboto", 12), "bg": "#424242", "fg": "black", "justify": "center"}

    def create_widgets(self):
        self.create_title()
        self.create_dice_frames()
        self.create_play_button()
        self.create_score_frame()

    def create_title(self):
        self.title_label = tk.Label(
            self.root, text="Yahtzee", **self.title_style)
        self.title_label.pack(pady=20)

    def create_dice_frames(self):
        self.player_dice_frame = self.create_dice_frame("You")
        self.bob_dice_frame = self.create_dice_frame(
            "Bob", button_state=tk.DISABLED)

    def create_dice_frame(self, player_name, button_command=None, button_state=tk.NORMAL):
        frame = tk.Frame(self.root, bg="#212121")
        frame.pack(pady=20)
        buttons, labels = self.create_dice_widgets(
            frame, button_command, button_state)
        return buttons, labels

    def create_dice_widgets(self, parent_frame, button_command=None, button_state=tk.NORMAL):
        buttons = []
        labels = []
        for i in range(5):
            button = tk.Button(
                parent_frame,
                text=f"{i + 1}",
                **self.button_style,
                width=4,
                command=lambda i=i: button_command(
                    i) if button_command else None,
                state=button_state,
            )
            button.grid(row=0, column=i, padx=10, pady=10)
            buttons.append(button)

            label = tk.Label(parent_frame, text="1", **
                             self.label_style, width=4)
            label.grid(row=1, column=i, padx=10, pady=10)
            labels.append(label)
        return buttons, labels

    def create_play_button(self):
        self.play_button_frame = tk.Frame(self.root, bg="#212121")
        self.play_button_frame.pack(pady=20)

        self.play_button = tk.Button(
            self.play_button_frame, text="Roll Dice", **self.button_style, command=self.play)
        self.play_button.pack(side=tk.RIGHT, padx=20)

    def create_score_frame(self):
        self.score_frame = tk.Frame(self.root, bg="#212121")
        self.score_frame.pack(pady=20, padx=20)

        self.create_score_widgets("Your Scores", 0)
        self.create_score_widgets("Bob's Scores", 2)

        self.player_score_label = self.create_score_label(
            len(self.game.get_scores("You")), 0)
        self.bob_score_label = self.create_score_label(
            len(self.game.get_scores("Bob")), 2)

    def create_score_widgets(self, text, col_offset):
        tk.Label(self.score_frame, text=text, **
                 self.label_style).grid(row=0, column=col_offset, padx=20, pady=10)
        for i, score_name in enumerate(self.game.get_scores("You").keys()):
            tk.Label(self.score_frame, text=score_name, **
                     self.label_style).grid(row=i + 1, column=col_offset, padx=20, pady=5)

    def create_score_label(self, score_count, col_offset):
        score_label = tk.Label(
            self.score_frame, text="Score: 0", **self.label_style)
        score_label.grid(row=score_count + 2, column=col_offset, pady=10)
        return score_label

    def play(self):
        if self.rolls_left > 0:
            self.game.player.roll_dice()
            self.update_dice_labels(
                self.player_dice_frame[1], self.game.get_player_dice_values())

            self.game.roll_bob_dice()
            self.update_dice_labels(
                self.bob_dice_frame[1], self.game.get_bob_dice_values())

            self.update_scores()
            self.enable_dice_buttons()

            self.rolls_left -= 1
            self.play_button.config(text=f"Roll Dice ({self.rolls_left})")

            if self.rolls_left == 0:
                self.play_button.config(state=tk.DISABLED)
                messagebox.showinfo("Yahtzee", "You've completed your rolls!")
        else:
            messagebox.showinfo("Yahtzee", "No more rolls left!")

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
            self.player_dice_frame[0][index].config(
                bg="#9400D3")  # Selected color
        else:
            self.player_dice_frame[0][index].config(
                bg="#007bff")  # Normal color

    def enable_dice_buttons(self):
        for button in self.player_dice_frame[0]:
            button.config(state=tk.NORMAL)
