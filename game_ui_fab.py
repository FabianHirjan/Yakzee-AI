import tkinter as tk
from game import Game


class DiceUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yakzee Dice Game")
        self.game = Game()

        self.roll_count = 0
        self.kept_indices = []
        self.selected_formations = set()  # selected formations

        self.player_frame = tk.Frame(root)
        self.player_frame.pack(side=tk.BOTTOM, padx=20, pady=20)

        self.bob_frame = tk.Frame(root)
        self.bob_frame.pack(side=tk.TOP, padx=20, pady=20)

        self.setup_player_ui()
        self.setup_bob_ui()
        self.setup_listbox()

        self.start_game()

    def setup_player_ui(self):
        self.player_dice = [self.create_dice_label(
            self.player_frame) for _ in range(5)]
        self.keep_buttons = [self.create_keep_button(i) for i in range(5)]
        self.player_button = tk.Button(
            self.player_frame, text="Roll", command=self.roll_dice)
        self.player_button.pack(side=tk.BOTTOM, pady=10)

    def create_dice_label(self, parent):
        label = tk.Label(parent, text=str(0), font=("Helvetica", 32))
        label.pack(side=tk.LEFT, padx=5)
        return label

    def create_keep_button(self, index):
        button = tk.Button(self.player_frame, text=f"Keep {index + 1}",
                           command=lambda: self.keep_dice(index))
        button.pack(side=tk.LEFT, padx=5)
        return button

    def setup_bob_ui(self):
        self.bob_dice = [self.create_dice_label(
            self.bob_frame) for _ in range(5)]

    def setup_listbox(self):
        self.listbox = tk.Listbox(
            self.root, width=50, height=30, font=("Helvetica", 12))
        self.listbox.pack(side=tk.RIGHT, padx=20, pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.select_formation)

    def roll_dice(self):
        if self.roll_count < 3:
            rolled_values = self.game.roll_dices(self.kept_indices)
            self.update_dice_display(rolled_values)
            possible_formations = self.game.player.suggest_formation(
                rolled_values)
            self.update_listbox(possible_formations)
            self.roll_count += 1
        else:
            print("You have reached the maximum number of rolls for this round.")

    def update_dice_display(self, rolled_values):
        for i, die in enumerate(self.player_dice):
            die.config(text=str(rolled_values[i]))

    def update_listbox(self, possible_formations):
        self.listbox.delete(0, tk.END)
        all_formations = self.game.player.formations.keys()
        for formation in all_formations:
            if formation in self.selected_formations:
                score = self.game.player.scores.get(formation, 0)
                self.listbox.insert(
                    tk.END, f"{formation} (Done, {score} points)")
            else:
                # check if it's a possible formation
                if any(formation == p[0] for p in possible_formations):
                    score = [p[1]
                             for p in possible_formations if p[0] == formation][0]
                    self.listbox.insert(
                        tk.END, f"{formation} (Score: {score})")
                else:
                    self.listbox.insert(tk.END, f"{formation} (Not Available)")

    def select_formation(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_formation = self.listbox.get(selected_index).split(
                " (")[0]
            if selected_formation not in self.selected_formations:
                self.selected_formations.add(selected_formation)
                self.game.player.keep_score(
                    selected_formation, self.game.kept_dice_values)
                print(
                    f"Formation '{selected_formation}' selected with score {self.game.player.scores[selected_formation]}.")
                self.roll_count = 0  # Reset roll count for next round
                self.start_next_turn()

    def keep_dice(self, index):
        if index in self.kept_indices:
            self.kept_indices.remove(index)
            self.game.keep_dice(index, keep=False)
            self.keep_buttons[index].config(text=f"Keep {index + 1}")
            print(f"Dice {index + 1} released.")
        else:
            self.kept_indices.append(index)
            self.game.keep_dice(index)
            self.keep_buttons[index].config(text=f"Unkeep {index + 1}")
            print(f"Dice {index + 1} kept.")

    def start_game(self):
        self.round = 1
        self.total_rounds = 13
        self.start_next_turn()

    def start_next_turn(self):
        if self.round <= self.total_rounds:
            print(f"\n--- Round {self.round} ---")
            print("Your turn:")
            self.play_player_turn()
        else:
            self.display_final_scores()

    def play_player_turn(self):
        self.roll_count = 0
        self.kept_indices = []
        self.update_dice_display([0] * 5)
        self.update_listbox([])
        self.player_button.config(state=tk.NORMAL)
        self.root.after(1000, self.play_bob_turn)

    def play_bob_turn(self):
        print("Bob's turn:")
        self.game.play_round(self.game.bob)
        self.round += 1
        self.start_next_turn()

    def display_final_scores(self):
        print("\nGame over! Final scores:")
        print(f"Your scores: {self.game.player.scores}")
        print(f"Bob's scores: {self.game.bob.scores}")
        print("Winner: You" if sum(self.game.player.scores.values())
              > sum(self.game.bob.scores.values()) else "Winner: Bob")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiceUI(root)
    root.mainloop()
