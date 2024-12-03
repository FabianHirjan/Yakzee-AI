# interactive.py

import tkinter as tk
import random
import numpy as np
from collections import Counter
import pickle
from collections import defaultdict

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

        # Inițializare scoruri pentru fiecare categorie
        for player in self.scores:
            for category in self.categories:
                self.scores[player][category] = None

        # Încărcarea tabelelor Q pentru AI
        self.q_table_dice = defaultdict(lambda: np.zeros(32))  # 2^5 posibile selecții de zaruri
        self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)))
        self.load_q_tables()

        # Parametri Q-Learning (doar pentru decizii, nu pentru antrenament)
        self.epsilon = 0.0  # AI-ul va folosi exclusiv exploatarea (0 explorare)

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
            print(f"Jucător: Toggle Zar {index + 1} la {'păstrat' if self.selected[index] else 'nepăstrat'}")

    def roll_dice(self):
        if self.rolls_left > 0 and self.state == "ROLLING":
            print(f"{self.current_player}: Aruncare {3 - self.rolls_left + 1}")
            for i in range(5):
                if not self.selected[i]:
                    self.dice[i] = random.randint(1, 6)
                self.dice_buttons[i].config(text=f"{self.dice[i]}")
            self.rolls_left -= 1
            self.message_label.config(
                text=f"{self.current_player}: {self.rolls_left} aruncări rămase"
            )
            print(f"{self.current_player}: Zaruri după aruncare: {self.dice}")
            if self.rolls_left == 0:
                self.set_state("CHOOSE_CATEGORY")

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
            print(f"{self.current_player} a ales categoria '{category}' și a obținut {score} puncte.")
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

    def calculate_score(self, category):
        counts = Counter(self.dice)
        values = list(counts.values())
        score = 0

        if category == "Three of a kind" and max(values) >= 3:
            score = sum(self.dice)
        elif category == "Four of a kind" and max(values) >= 4:
            score = sum(self.dice)
        elif category == "Full House" and sorted(values) == [2, 3]:
            score = 25
        elif category == "Small Straight" and self.has_straight(4):
            score = 30
        elif category == "Large Straight" and self.has_straight(5):
            score = 40
        elif category == "Yahtzee" and max(values) == 5:
            score = 50
        elif category == "Chance":
            score = sum(self.dice)

        return score

    def has_straight(self, length):
        unique = sorted(set(self.dice))
        for i in range(len(unique) - length + 1):
            if unique[i:i + length] == list(range(unique[i], unique[i] + length)):
                return True
        return False

    def update_score_table(self):
        for player, data in self.scores.items():
            for category, score in data.items():
                if category != "labels":
                    label = self.scores[player]["labels"][category]
                    label.config(text=str(score) if score is not None else "-")

    def set_state(self, state):
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
                print(f"{self.current_player}: Turul începe. Zaruri resetate.")
            elif self.current_player == "AI":
                self.roll_button.config(state="disabled")
                self.end_turn_button.config(state="disabled")
                self.message_label.config(text=f"{self.current_player}: Este turul AI-ului.")
                self.master.after(1000, self.ai_turn)  # Așteaptă 1 secundă înainte de a începe turul AI
        elif state == "CHOOSE_CATEGORY":
            self.roll_button.config(state="disabled")
            if self.current_player == "Jucător":
                self.end_turn_button.config(state="normal")
                self.message_label.config(text="Alege o categorie pentru a puncta!")
                self.choose_category()
            elif self.current_player == "AI":
                self.master.after(1000, self.ai_choose_category)  # Așteaptă 1 secundă înainte de a alege categoria
        elif state == "SWITCH_PLAYER":
            self.current_player = "AI" if self.current_player == "Jucător" else "Jucător"
            self.set_state("ROLLING")
        elif state == "GAME_OVER":
            try:
                # Calcularea scorului total pentru fiecare jucător, excluzând "labels"
                total_scores = {}
                for player in self.scores:
                    total_scores[player] = sum(
                        v for k, v in self.scores[player].items() if k != "labels" and v is not None
                    )
                # Determinarea câștigătorului
                winner = max(total_scores, key=total_scores.get)
                self.message_label.config(text=f"Joc terminat! Câștigător: {winner} cu {total_scores[winner]} puncte.")
                print(f"Joc terminat! Câștigător: {winner} cu {total_scores[winner]} puncte.")
            except ValueError:
                # În caz de egalitate sau alte probleme
                self.message_label.config(text=f"Joc terminat! Egalitate.")
                print("Joc terminat! Egalitate.")
            self.roll_button.config(state="disabled")
            self.end_turn_button.config(state="disabled")

    def is_game_over(self):
        return all(
            self.scores[player][cat] is not None 
            for player in self.scores 
            for cat in self.categories
        )

    def ai_turn(self):
        print("AI începe turul.")
        while self.rolls_left > 0:
            state = self.get_state_dice()

            if state not in self.q_table_dice:
                self.q_table_dice[state] = np.zeros(32)  # 2^5 posibile selecții

            # Decizie pentru selecția zarurilor pe baza Q-Table
            selected = self.choose_dice_to_keep(state)
            self.selected = selected

            print(f"AI: Zaruri păstrate: {self.selected}")

            # Aruncă zarurile care nu sunt selectate
            for i in range(5):
                if not self.selected[i]:
                    self.dice[i] = random.randint(1, 6)

            print(f"AI a aruncat zarurile: {self.dice}")
            self.update_dice_buttons()
            self.rolls_left -= 1
            self.message_label.config(
                text=f"{self.current_player}: {self.rolls_left} aruncări rămase"
            )
            self.master.update_idletasks()

            if self.rolls_left == 0:
                self.set_state("CHOOSE_CATEGORY")

    def ai_choose_category(self):
        state = self.get_state_category()
        if state not in self.q_table_category:
            self.q_table_category[state] = np.zeros(len(self.categories))

        available_categories = [i for i, cat in enumerate(self.categories) if self.scores["AI"][cat] is None]

        if not available_categories:
            print("Nu mai sunt categorii disponibile pentru AI.")
            self.set_state("GAME_OVER")
            return

        # Alege categoria pe baza valorilor Q din tabelul Q
        q_values = self.q_table_category[state]
        filtered_q = [q_values[i] if i in available_categories else -np.inf for i in range(len(self.categories))]
        action = np.argmax(filtered_q)
        chosen_category = self.categories[action]

        print(f"AI decide să aleagă categoria '{chosen_category}'")
        reward = self.calculate_score(chosen_category)
        print(f"AI a înscris {reward} puncte în categoria '{chosen_category}'")
        self.scores["AI"][chosen_category] = reward
        self.update_score_table()
        if self.is_game_over():
            self.set_state("GAME_OVER")
        else:
            self.set_state("SWITCH_PLAYER")

    def choose_dice_to_keep(self, state):
        """Alege zarurile care trebuie păstrate bazat pe Q-Table pentru selecția zarurilor."""
        q_values = self.q_table_dice[state]
        best_action = np.argmax(q_values)
        binary = bin(best_action)[2:].zfill(5)
        selected = [bit == '1' for bit in binary]
        print(f"AI: State {state}, Best Action {best_action} ({binary}), Selected {selected}")
        return selected

    def get_state_dice(self):
        """Reprezentarea stării pentru selecția zarurilor."""
        grouped_dice = self.group_dice(self.dice)
        return tuple(grouped_dice), self.rolls_left

    def get_state_category(self):
        """Reprezentarea stării pentru alegerea categoriei."""
        grouped_dice = self.group_dice(self.dice)
        return tuple(grouped_dice)

    def group_dice(self, dice):
        """Reprezintă starea zarurilor ca un vector al frecvenței valorilor."""
        counts = Counter(dice)
        grouped_state = [counts[i] for i in range(1, 7)]
        return grouped_state

    def update_dice_buttons(self):
        for i in range(5):
            self.dice_buttons[i].config(text=f"{self.dice[i]}")

    def load_q_tables(self, filename_dice="q_table_dice_final.pkl", filename_category="q_table_category_final.pkl"):
        try:
            with open(filename_dice, "rb") as f:
                self.q_table_dice = pickle.load(f)
            print(f"Tabelul Q pentru zaruri a fost încărcat din: {filename_dice}")
        except FileNotFoundError:
            print(f"Fișierul {filename_dice} nu a fost găsit. AI-ul va învăța de la zero.")
            self.q_table_dice = defaultdict(lambda: np.zeros(32))

        try:
            with open(filename_category, "rb") as f:
                self.q_table_category = pickle.load(f)
            print(f"Tabelul Q pentru categorii a fost încărcat din: {filename_category}")
        except FileNotFoundError:
            print(f"Fișierul {filename_category} nu a fost găsit. AI-ul va învăța de la zero.")
            self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)))

    def save_q_tables(self, filename_dice="q_table_dice_final.pkl", filename_category="q_table_category_final.pkl"):
        """Salvează ambele tabele Q într-un fișier."""
        with open(filename_dice, "wb") as f:
            pickle.dump(dict(self.q_table_dice), f)
        with open(filename_category, "wb") as f:
            pickle.dump(dict(self.q_table_category), f)
        print(f"Tabelele Q au fost salvate în {filename_dice} și {filename_category}")

# Lansare aplicație
if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveYahtzeeGame(root)
    root.mainloop()
