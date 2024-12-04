import tkinter as tk
import random
import pickle
import numpy as np
from collections import Counter, defaultdict


class InteractiveYahtzeeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Yahtzee - Joc Interactiv")
        self.master.geometry("900x600")
        self.state = "START"
        self.rolls_left = 3
        self.dice = [0] * 5
        self.selected = [False] * 5
        self.scores = {"Jucător": {}, "AI": {}}
        self.current_player = "Jucător"
        self.categories = [
            "Three of a kind",
            "Four of a kind",
            "Full House",
            "Small Straight",
            "Large Straight",
            "Yahtzee",
            "Chance",
        ]

        # Inițializare scoruri
        for player in self.scores:
            for category in self.categories:
                self.scores[player][category] = None

        # Încărcarea tabelelor Q
        self.q_table_dice = defaultdict(lambda: np.zeros(32))
        self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)))
        self.load_trained_ai()

        # Parametri AI
        self.epsilon = 0.0  # Exclusiv exploatare

        self.create_widgets()
        self.set_state("ROLLING")

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Yahtzee - Joc Interactiv", font=("Arial", 20))
        self.title_label.pack()

        self.dice_frame = tk.Frame(self.master)
        self.dice_frame.pack(pady=10)

        self.dice_buttons = []
        for i in range(5):
            btn = tk.Button(
                self.dice_frame,
                text="Zar 1",
                font=("Arial", 14),
                width=8,
                height=2,
                command=lambda i=i: self.toggle_dice(i),
            )
            btn.grid(row=0, column=i, padx=5)
            self.dice_buttons.append(btn)

        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(pady=10)

        self.roll_button = tk.Button(
            self.control_frame, text="Aruncă zarurile", font=("Arial", 14), command=self.roll_dice
        )
        self.roll_button.pack(side="left", padx=10)

        self.end_turn_button = tk.Button(
            self.control_frame, text="Alege categorie", font=("Arial", 14), command=self.choose_category, state="disabled"
        )
        self.end_turn_button.pack(side="left", padx=10)

        self.message_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.message_label.pack(pady=10)

        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(pady=20)

        self.player_score_frame = self.create_score_table("Jucător", 0)
        self.ai_score_frame = self.create_score_table("AI", 1)

    def create_score_table(self, player, column):
        frame = tk.Frame(self.score_frame, borderwidth=2, relief="groove")
        frame.grid(row=0, column=column, padx=10, sticky="n")

        title = tk.Label(frame, text=f"Scor {player}", font=("Arial", 16))
        title.pack()

        self.scores[player]["labels"] = {}

        for category in self.categories:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=2)

            label = tk.Label(row, text=category, font=("Arial", 12), width=20, anchor="w")
            label.pack(side="left")

            score_label = tk.Label(row, text="-", font=("Arial", 12), width=6, anchor="e")
            score_label.pack(side="right")

            self.scores[player]["labels"][category] = score_label

        return frame

    def toggle_dice(self, index):
        if self.state == "ROLLING" and self.current_player == "Jucător":
            self.selected[index] = not self.selected[index]
            self.dice_buttons[index].config(
                relief="sunken" if self.selected[index] else "raised"
            )

    def roll_dice(self):
        if self.rolls_left > 0 and self.state == "ROLLING":
            for i in range(5):
                if not self.selected[i]:
                    self.dice[i] = random.randint(1, 6)
                self.dice_buttons[i].config(text=f"{self.dice[i]}")
            self.rolls_left -= 1
            self.message_label.config(
                text=f"{self.current_player}: {self.rolls_left} aruncări rămase"
            )
            if self.rolls_left == 0:
                self.set_state("CHOOSE_CATEGORY")

    def update_dice_buttons(self):
        for i in range(5):
            self.dice_buttons[i].config(text=f"{self.dice[i]}")

    def choose_category(self):
        if self.state != "CHOOSE_CATEGORY":
            return

        def score_category(category):
            if self.scores[self.current_player][category] is not None:
                self.message_label.config(text=f"Categoria {category} a fost deja folosită!")
                return

            score = self.calculate_score(category)
            self.scores[self.current_player][category] = score
            self.update_score_table()
            if self.is_game_over():
                self.set_state("GAME_OVER")
            else:
                self.set_state("SWITCH_PLAYER")

        self.message_label.config(text="Alege o categorie pentru a puncta!")
        for category, label in self.scores[self.current_player]["labels"].items():
            if self.scores[self.current_player][category] is None:
                label.bind("<Button-1>", lambda e, c=category: score_category(c))
            else:
                label.unbind("<Button-1>")

    def set_state(self, state):
        print(f"Schimbare stare: {self.state} -> {state}")
        self.state = state
        if state == "ROLLING":
            self.rolls_left = 3
            self.selected = [False] * 5
            for btn in self.dice_buttons:
                btn.config(relief="raised")
            if self.current_player == "Jucător":
                self.roll_button.config(state="normal")
                self.end_turn_button.config(state="disabled")
                self.message_label.config(text=f"{self.current_player}: Aruncă zarurile!")
            elif self.current_player == "AI":
                self.roll_button.config(state="disabled")
                self.end_turn_button.config(state="disabled")
                self.master.after(1000, self.ai_turn)
        elif state == "CHOOSE_CATEGORY":
            self.roll_button.config(state="disabled")
            if self.current_player == "Jucător":
                self.end_turn_button.config(state="normal")
                self.choose_category()
            elif self.current_player == "AI":
                self.master.after(1000, self.ai_choose_category)
        elif state == "SWITCH_PLAYER":
            self.current_player = "AI" if self.current_player == "Jucător" else "Jucător"
            self.set_state("ROLLING")
        elif state == "GAME_OVER":
            total_scores = {
                player: sum(v for k, v in self.scores[player].items() if k != "labels" and v is not None)
                for player in self.scores
            }
            winner = max(total_scores, key=total_scores.get)
            self.message_label.config(text=f"Joc terminat! Câștigător: {winner} cu {total_scores[winner]} puncte.")
            self.roll_button.config(state="disabled")
            self.end_turn_button.config(state="disabled")

    def update_score_table(self):
        """Actualizează tabelul de scoruri pentru fiecare jucător."""
        for player, data in self.scores.items():
            for category, score in data.items():
                if category != "labels":  # Ignoră cheia 'labels'
                    label = self.scores[player]["labels"][category]
                    label.config(text=str(score) if score is not None else "-")

    def is_game_over(self):
        """Verifică dacă jocul s-a terminat (toate categoriile sunt completate pentru toți jucătorii)."""
        for player in self.scores:
            for category, score in self.scores[player].items():
                if category != "labels" and score is None:
                    return False
        return True



    def ai_turn(self):
        print("AI începe turul.")
        # Roll dice at the start of the AI's turn
        for i in range(5):
            self.dice[i] = random.randint(1, 6)
        self.update_dice_buttons()
        self.rolls_left -= 1

        while self.rolls_left > 0:
            state = self.get_state_dice()
            # Check if state exists in q_table_dice
            if state not in self.q_table_dice:
                print(f"Starea {state} nu există în q_table_dice. Inițializare...")
                self.q_table_dice[state] = np.zeros(32)
            q_values = self.q_table_dice[state]
            action = np.argmax(q_values)
            self.selected = self.action_to_dice_selection(action)
            print(f"AI: Zaruri păstrate: {[self.dice[i] if self.selected[i] else None for i in range(5)]}")
            for i in range(5):
                if not self.selected[i]:
                    self.dice[i] = random.randint(1, 6)
            print(f"AI a aruncat zarurile: {self.dice}")
            self.update_dice_buttons()
            self.rolls_left -= 1

        self.set_state("CHOOSE_CATEGORY")



    def ai_choose_category(self):
        state = self.get_state_category()

        if state not in self.q_table_category:
            print(f"Starea {state} nu există în q_table_category. Inițializare...")
            self.q_table_category[state] = np.zeros(len(self.categories))

        available_categories = [i for i, cat in enumerate(self.categories) if self.scores["AI"][cat] is None]
        if not available_categories:
            print("Nu mai sunt categorii disponibile pentru AI.")
            self.set_state("GAME_OVER")
            return

        q_values = self.q_table_category[state]
        filtered_q = [q_values[i] if i in available_categories else -np.inf for i in range(len(self.categories))]
        action = np.argmax(filtered_q)
        chosen_category = self.categories[action]

        print(f"AI a ales categoria '{chosen_category}'.")
        reward = self.calculate_score(chosen_category)
        self.scores["AI"][chosen_category] = reward
        self.update_score_table()

        if self.is_game_over():
            self.set_state("GAME_OVER")
        else:
            self.set_state("SWITCH_PLAYER")


    def calculate_score(self, category):
        counts = Counter(self.dice)
        values = list(counts.values())
        if category == "Three of a kind" and max(values) >= 3:
            return sum(self.dice)
        elif category == "Four of a kind" and max(values) >= 4:
            return sum(self.dice)
        elif category == "Full House" and sorted(values) == [2, 3]:
            return 25
        elif category == "Small Straight" and self.has_straight(4):
            return 30
        elif category == "Large Straight" and self.has_straight(5):
            return 40
        elif category == "Yahtzee" and max(values) == 5:
            return 50
        elif category == "Chance":
            return sum(self.dice)
        return 0

    def has_straight(self, length):
        unique = sorted(set(self.dice))
        for i in range(len(unique) - length + 1):
            if unique[i:i + length] == list(range(unique[i], unique[i] + length)):
                return True
        return False

    def get_state_dice(self):
        counts = Counter(self.dice)
        return tuple(counts[i] for i in range(1, 7)), self.rolls_left

    def get_state_category(self):
        counts = Counter(self.dice)
        return tuple(counts[i] for i in range(1, 7))

    def action_to_dice_selection(self, action):
        binary = bin(action)[2:].zfill(5)
        return [bit == '1' for bit in binary]

    def load_trained_ai(self, filename_dice="q_table_dice_final.pkl", filename_category="q_table_category_final.pkl"):
        try:
            with open(filename_dice, "rb") as f:
                loaded_q_table_dice = pickle.load(f)
            self.q_table_dice = defaultdict(lambda: np.zeros(32), loaded_q_table_dice)
        except FileNotFoundError:
            print(f"Fișierul {filename_dice} nu a fost găsit.")

        try:
            with open(filename_category, "rb") as f:
                loaded_q_table_category = pickle.load(f)
            self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)), loaded_q_table_category)
        except FileNotFoundError:
            print(f"Fișierul {filename_category} nu a fost găsit.")



if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveYahtzeeGame(root)
    root.mainloop()
