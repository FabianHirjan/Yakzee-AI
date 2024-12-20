import tkinter as tk
import random
import pickle
import numpy as np
from collections import Counter, defaultdict

class InteractiveYahtzeeGame:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Yahtzee")
        self.master.geometry("900x600")  
        self.state = "START"  
        self.rolls_left = 3  
        self.dice = [0] * 5 
        self.selected = [False] * 5  
        self.scores = {"Player": {}, "AI": {}}  
        self.current_player = "Player" 
        self.categories = [ 
            "Three of a kind",
            "Four of a kind",
            "Full House",
            "Small Straight",
            "Large Straight",
            "Yahtzee",
            "Chance",
        ]

       
        for player in self.scores:
            for category in self.categories:
                self.scores[player][category] = None

       
        self.q_table_dice = defaultdict(lambda: np.zeros(32)) 
        self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)))
        self.load_trained_ai()

       
        self.epsilon = 0.0  

        
        self.display_policy()

        
        self.create_widgets()
        self.set_state("ROLLING")  

    def display_dice_policy(self):
       
        print("=== Dice Selection Policy ===")
        for state, q_values in self.q_table_dice.items():
            best_action = np.argmax(q_values)  
            dice_selection = self.action_to_dice_selection(best_action)
            print(f"State: {state} -> Action: {best_action}, Dice Selection: {dice_selection}")

    def display_category_policy(self):
       
        print("=== Category Selection Policy ===")
        for state, q_values in self.q_table_category.items():
            best_action = np.argmax(q_values) 
            chosen_category = self.categories[best_action]
            print(f"State: {state} -> Action: {best_action}, Chosen Category: {chosen_category}")

    def display_policy(self):
       
        print("\n=== Complete Policy ===")
        self.display_dice_policy()
        self.display_category_policy()

    def create_widgets(self):
        
        self.title_label = tk.Label(self.master, text="Yahtzee", font=("Arial", 20))
        self.title_label.pack()

        
        self.dice_frame = tk.Frame(self.master)
        self.dice_frame.pack(pady=10)

        self.dice_buttons = []  
        for i in range(5):
            btn = tk.Button(
                self.dice_frame,
                text="Die 1", 
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
            self.control_frame, text="Roll Dice", font=("Arial", 14), command=self.roll_dice
        )
        self.roll_button.pack(side="left", padx=10)

        self.end_turn_button = tk.Button(
            self.control_frame, text="Choose Category", font=("Arial", 14), command=self.choose_category, state="disabled"
        )
        self.end_turn_button.pack(side="left", padx=10)

        
        self.message_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.message_label.pack(pady=10)

        
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(pady=20)

        
        self.player_score_frame = self.create_score_table("Player", 0)
        self.ai_score_frame = self.create_score_table("AI", 1)

    def create_score_table(self, player, column):
       
        frame = tk.Frame(self.score_frame, borderwidth=2, relief="groove")
        frame.grid(row=0, column=column, padx=10, sticky="n")

        
        title = tk.Label(frame, text=f"Score {player}", font=("Arial", 16))
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
       
        if self.state == "ROLLING" and self.current_player == "Player":
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
                text=f"{self.current_player}: {self.rolls_left} rolls left"
            )
            if self.rolls_left == 0:
                self.set_state("CHOOSE_CATEGORY")

    def update_dice_buttons(self):
        
        for i in range(5):
            self.dice_buttons[i].config(text=f"{self.dice[i]}")

    def choose_category(self):
        

        def score_category(category):
           
            if self.scores[self.current_player][category] is not None:
                self.message_label.config(text=f"Category {category} has already been used!")
                return

            score = self.calculate_score(category)
            self.scores[self.current_player][category] = score
            self.update_score_table()
            if self.is_game_over():
                self.set_state("GAME_OVER")
            else:
                self.set_state("SWITCH_PLAYER")

        self.message_label.config(text="Choose a category.")
        for category, label in self.scores[self.current_player]["labels"].items():
            if self.scores[self.current_player][category] is None:
                label.bind("<Button-1>", lambda e, c=category: score_category(c))
            else:
                label.unbind("<Button-1>")

    def set_state(self, state):
        
        print(f"State change: {self.state} -> {state}")
        self.state = state
        if state == "ROLLING":
            
            self.rolls_left = 3
            self.selected = [False] * 5
            for btn in self.dice_buttons:
                btn.config(relief="raised")
            if self.current_player == "Player":
                self.roll_button.config(state="normal")
                self.end_turn_button.config(state="disabled")
                self.message_label.config(text=f"{self.current_player}: Roll the dice!")
            elif self.current_player == "AI":
                self.roll_button.config(state="disabled")
                self.end_turn_button.config(state="disabled")
                self.master.after(1000, self.ai_turn)
        elif state == "CHOOSE_CATEGORY":
            self.roll_button.config(state="disabled")
            if self.current_player == "Player":
                self.end_turn_button.config(state="normal")
                self.choose_category()
            elif self.current_player == "AI":
                self.master.after(1000, self.ai_choose_category)
        elif state == "SWITCH_PLAYER":
            self.current_player = "AI" if self.current_player == "Player" else "Player"
            self.set_state("ROLLING")
        elif state == "GAME_OVER":
            total_scores = {
                player: sum(v for k, v in self.scores[player].items() if k != "labels" and v is not None)
                for player in self.scores
            }
            winner = max(total_scores, key=total_scores.get)
            self.message_label.config(text=f"Game over! Winner: {winner} with {total_scores[winner]} points.")
            self.roll_button.config(state="disabled")
            self.end_turn_button.config(state="disabled")

    def update_score_table(self):
        
        for player, data in self.scores.items():
            for category, score in data.items():
                if category != "labels":
                    label = self.scores[player]["labels"][category]
                    label.config(text=str(score) if score is not None else "-")

    def is_game_over(self):
        
        for player in self.scores:
            for category, score in self.scores[player].items():
                if category != "labels" and score is None:
                    return False
        return True

    def ai_turn(self):
        
        print("AI starts its turn.")
        for i in range(5):
            self.dice[i] = random.randint(1, 6)
        self.update_dice_buttons()
        self.rolls_left -= 1

        while self.rolls_left > 0:
            state = self.get_state_dice()
            if state not in self.q_table_dice:
                print(f"State {state} does not exist in q_table_dice. Initializing...")
                self.q_table_dice[state] = np.zeros(32)
            q_values = self.q_table_dice[state]
            action = np.argmax(q_values)
            self.selected = self.action_to_dice_selection(action)
            print(f"AI: Dice kept: {[self.dice[i] if self.selected[i] else None for i in range(5)]}")
            for i in range(5):
                if not self.selected[i]:
                    self.dice[i] = random.randint(1, 6)
            print(f"AI rolled: {self.dice}")
            self.update_dice_buttons()
            self.rolls_left -= 1

        self.set_state("CHOOSE_CATEGORY")

    def ai_choose_category(self):
        
        state = self.get_state_category()

        if state not in self.q_table_category:
            print(f"State {state} does not exist in q_table_category. Initializing...")
            self.q_table_category[state] = np.zeros(len(self.categories))

        available_categories = [i for i, cat in enumerate(self.categories) if self.scores["AI"][cat] is None]
        if not available_categories:
            print("No categories available for AI.")
            self.set_state("GAME_OVER")
            return

        q_values = self.q_table_category[state]
        filtered_q = [q_values[i] if i in available_categories else -np.inf for i in range(len(self.categories))]
        action = np.argmax(filtered_q)
        chosen_category = self.categories[action]

        print(f"AI chose category '{chosen_category}'.")
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
            print(f"File {filename_dice} not found.")

        try:
            with open(filename_category, "rb") as f:
                loaded_q_table_category = pickle.load(f)
            self.q_table_category = defaultdict(lambda: np.zeros(len(self.categories)), loaded_q_table_category)
        except FileNotFoundError:
            print(f"File {filename_category} not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveYahtzeeGame(root)
    root.mainloop()
