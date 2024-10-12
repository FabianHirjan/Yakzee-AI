import tkinter as tk
from yahtzee import YahtzeeGame
from tkinter import ttk


class YahtzeeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yahtzee")

        self.root.geometry("1200x800")
        self.root.configure(bg="#2E3B4E")

        self.game = YahtzeeGame()

        self.label_style = {
            "font": ("Arial", 18), "bg": "#4E5D6C", "fg": "white"}
        self.button_style = {"font": (
            "Arial", 18), "bg": "#FF00FF", "fg": "white", "activebackground": "#FFA500"}

        self.dice_frame = tk.Frame(self.root, bg="#2E3B4E")
        self.dice_frame.pack(side=tk.TOP, pady=20)

        self.dice_buttons, self.dice_labels = self.create_dice_widgets(
            row_offset=0, button_command=self.toggle_dice_selection)
        self.bob_dice_labels = self.create_dice_widgets(
            row_offset=2, button_state=tk.DISABLED)[1]

        self.play_button = tk.Button(
            self.root, text="Roll Dice", **self.button_style, command=self.play)
        self.play_button.pack(pady=20)

        self.score_frame = tk.Frame(self.root, bg="#2E3B4E")
        self.score_frame.place(x=850, y=50)  # dreapta sus

        self.create_score_frame()

        self.root.mainloop()

    def create_dice_widgets(self, row_offset=0, button_command=None, button_state=tk.NORMAL):
        """Creează butoanele și etichetele pentru zarurile jucătorului și Bob"""
        buttons = []
        labels = []
        for i in range(5):
            button = tk.Button(self.dice_frame, text=f"Die {i + 1}", **self.button_style,
                               width=5, command=lambda i=i: button_command(i) if button_command else None,
                               state=button_state)
            button.grid(row=row_offset, column=i, padx=5, pady=5)
            buttons.append(button)

            label = tk.Label(self.dice_frame, text="1",
                             **self.label_style, width=5)
            label.grid(row=row_offset + 1, column=i, padx=5, pady=5)
            labels.append(label)
        return buttons, labels

    def create_score_frame(self):
        """Creează frame-ul și etichetele pentru scoruri"""
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
        """Creează etichetele și câmpurile de scor pentru un jucător"""
        tk.Label(self.score_frame, text=text, **
                 self.label_style).grid(row=0, column=col_offset, padx=10)

        score_entries = {}
        for i, score_name in enumerate(self.game.get_player_scores().keys()):
            tk.Label(self.score_frame, text=score_name, **
                     self.label_style).grid(row=i + 1, column=col_offset, padx=10, pady=5)
            score_entry = tk.Entry(
                self.score_frame, font=("Arial", 16), width=5)
            score_entry.grid(row=i + 1, column=col_offset + 1, padx=10)
            score_entries[score_name] = score_entry

        return score_entries

    def play(self):
        """Execută o rundă de zaruri pentru jucător și Bob"""
        self.game.player.roll_dice()
        self.update_dice_labels(
            self.dice_labels, self.game.get_player_dice_values())

        self.game.roll_bob_dice()
        self.update_dice_labels(self.bob_dice_labels,
                                self.game.get_bob_dice_values())

        self.update_scores()

    def update_dice_labels(self, labels, values):
        """Actualizează valorile afișate pe zaruri"""
        for label, value in zip(labels, values):
            label.config(text=str(value))

    def update_scores(self):
        """Actualizează scorurile jucătorilor"""
        self.player_score_label.config(
            text="Score: " + str(sum(self.game.get_player_dice_values())))
        self.bob_score_label.config(
            text="Score: " + str(sum(self.game.get_bob_dice_values())))

    def toggle_dice_selection(self, index):
        """Selectează/deselectează zarul jucătorului și actualizează culoarea butonului"""
        self.game.player.toggle_dice_selection(index)
        if self.game.player.selected_dice[index]:
            self.dice_buttons[index].config(bg='#9400D3')
        else:
            self.dice_buttons[index].config(bg='#FF00FF')
