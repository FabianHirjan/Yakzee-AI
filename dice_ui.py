from collections import Counter
import tkinter as tk
from tkinter import messagebox
from dice import Dice
from player import Player
import random

class YahtzeeGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahtzee Game")

        self.no_of_dices = 5
        self.dices = [Dice(6) for _ in range(self.no_of_dices)]  
        self.bob_dices = [Dice(6) for _ in range(self.no_of_dices)]  
        self.kept_dice_values = [None] * self.no_of_dices 
        self.bob_dice_values = [None] * self.no_of_dices 
        self.kept_dices = []  

        self.player = Player("You")  
        self.bob = Player("Bob")  

        self.rolls_left = 3  
        self.total_formations = 8  # Assuming 8 formations
        self.rounds_played = 0  # Track the number of rounds played
        self.player_turn_complete = False  # To track if the player has completed all formations


        self.dice_labels = []
        self.bob_dice_labels = []  
        self.dice_buttons = []
        self.create_widgets()
        self.update_dice_display()

    def create_widgets(self):
        tk.Label(self.root, text="Your Dice:").grid(row=0, column=0, columnspan=5)

        for i in range(self.no_of_dices):
            dice_label = tk.Label(self.root, text="⚀", font=("Helvetica", 50), width=3)
            dice_label.grid(row=1, column=i, padx=10, pady=10)
            self.dice_labels.append(dice_label)

            dice_button = tk.Button(self.root, text="Keep", command=lambda i=i: self.toggle_keep_dice(i))
            dice_button.grid(row=2, column=i)
            self.dice_buttons.append(dice_button)

        self.roll_button = tk.Button(self.root, text="Roll", command=self.roll_dices)
        self.roll_button.grid(row=3, column=0, columnspan=5)

        tk.Label(self.root, text="Bob's Dice:").grid(row=4, column=0, columnspan=5)

        for i in range(self.no_of_dices):
            bob_dice_label = tk.Label(self.root, text="⚀", font=("Helvetica", 50), width=3)
            bob_dice_label.grid(row=5, column=i, padx=10, pady=10)
            self.bob_dice_labels.append(bob_dice_label)

        self.rolls_left_label = tk.Label(self.root, text=f"Rolls Left: {self.rolls_left}", font=("Helvetica", 14))
        self.rolls_left_label.grid(row=6, column=0, columnspan=5)

        self.formations_label = tk.Label(self.root, text="Formations: None", font=("Helvetica", 14))
        self.formations_label.grid(row=7, column=0, columnspan=5)

        self.scores_label = tk.Label(self.root, text="Your Score: 0\nBob's Score: 0", font=("Helvetica", 14))
        self.scores_label.grid(row=8, column=0, columnspan=5)

        self.player_formations_frame = tk.Frame(self.root)
        self.player_formations_frame.grid(row=9, column=0, columnspan=5)

        self.select_formation_button = tk.Button(self.root, text="Select Formation", command=self.select_formation_button_clicked)
        self.select_formation_button.grid(row=3, column=5)  # Adjust the column/row position to suit your layout
        self.select_formation_button.config(state=tk.DISABLED)  # Disable until they roll


        self.update_formations_display()

    def roll_dices(self):
        if self.rolls_left > 0:
            self.animate_roll_dices() 
            self.roll_button.config(state=tk.DISABLED) 

    def animate_roll_dices(self, iteration=0, max_iterations=10):
        """Simulate dice rolling animation with random values before showing the final roll."""
        if iteration < max_iterations:
            for i in range(self.no_of_dices):
                if i not in self.kept_dices:  
                    random_value = random.randint(1, 6)
                    dice_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
                    self.dice_labels[i].config(text=dice_symbols[random_value - 1])

            self.root.after(100, self.animate_roll_dices, iteration + 1, max_iterations)
        else:
            self.final_roll()

    def final_roll(self):
        """Perform the final dice roll and update the display."""
        for i, dice in enumerate(self.dices):
            if i not in self.kept_dices:
                self.kept_dice_values[i] = dice.roll()

        self.update_dice_display()
        self.rolls_left -= 1
        self.rolls_left_label.config(text=f"Rolls Left: {self.rolls_left}")

        if self.rolls_left == 0:
            self.roll_button.config(state=tk.DISABLED)  # Disable roll after all rolls used
        else:
            self.roll_button.config(state=tk.NORMAL)  # Enable the roll button until rolls are exhausted

        # Allow selection of formation after each roll
        possible_formations = self.player.suggest_formation(self.kept_dice_values)
        self.display_possible_formations(possible_formations)
        
        # Enable "Select Formation" button after each roll
        self.select_formation_button.config(state=tk.NORMAL)

    def update_dice_display(self):
        dice_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']  
        for i, dice_value in enumerate(self.kept_dice_values):
            if dice_value is not None:
                self.dice_labels[i].config(text=dice_symbols[dice_value - 1])
            else:
                self.dice_labels[i].config(text="⚀") 

            if i in self.kept_dices:
                self.dice_labels[i].config(bg="lightblue")
            else:
                self.dice_labels[i].config(bg="SystemButtonFace")  

    def update_bob_dice_display(self, bob_dice_values):
        """Update the dice display for Bob (the bot)."""
        dice_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        for i, dice_value in enumerate(bob_dice_values):
            if dice_value is not None:
                self.bob_dice_labels[i].config(text=dice_symbols[dice_value - 1])
            else:
                self.bob_dice_labels[i].config(text="⚀")

    def toggle_keep_dice(self, dice_index):
        if dice_index in self.kept_dices:
            self.kept_dices.remove(dice_index)
            self.dice_buttons[dice_index].config(text="Keep")
        else:
            self.kept_dices.append(dice_index)
            self.dice_buttons[dice_index].config(text="Unkeep")
        self.update_dice_display()

    def reset_dices(self):
        """Reset the dice and UI elements for a new turn."""
        self.rolls_left = 3
        self.roll_button.config(state=tk.NORMAL)
        self.rolls_left_label.config(text=f"Rolls Left: {self.rolls_left}")
        
        # Reset dice values
        self.kept_dice_values = [None] * self.no_of_dices
        self.bob_dice_values = [None] * self.no_of_dices
        self.kept_dices = []  # Clear kept dice

        # Reset the dice buttons to "Keep"
        for i in range(self.no_of_dices):
            self.dice_buttons[i].config(text="Keep")  # Reset button text
            self.dice_buttons[i].config(state=tk.NORMAL)  # Re-enable the buttons

        self.update_dice_display()
        self.update_bob_dice_display([None] * self.no_of_dices)


    def end_turn(self):
        """End the current player's turn and check if the game should end."""
        print("Ending turn.")
        
        # Check if the player has filled all their formations
        if self.are_all_formations_filled(player=True):
            print("Player has filled all formations.")
            self.player_turn_complete = True  # Mark player's turn as complete

        # If the player has completed, let Bob take one last turn and end the game
        if self.player_turn_complete:
            print("Player is done. Bob is making the final move.")
            self.bob_turn(final_turn=True)  # Bob takes the final move
            self.end_game()  # After Bob's final move, end the game
        else:
            # Reset the dices for the next turn
            self.reset_dices()
            self.root.after(100, self.bob_turn)  # Bob's regular turn after player's turn



  
    def are_all_formations_filled(self, player=False):
        """Check if all formations have been filled for the player or Bob."""
        all_formations = ["Yahtzee!", "Four of a Kind", "Full House", "Three of a Kind",
                        "Large Straight", "Small Straight", "Two Pairs", "One Pair"]
        
        if player:
            # Check if all formations are filled for the player
            return all(self.player.scores.get(formation) is not None for formation in all_formations)
        else:
            # Check if all formations are filled for both the player and Bob
            player_all_filled = all(self.player.scores.get(formation) is not None for formation in all_formations)
            bob_all_filled = all(self.bob.scores.get(formation) is not None for formation in all_formations)

            print(f"Player All Formations Filled: {player_all_filled}, Bob All Formations Filled: {bob_all_filled}")

            return player_all_filled and bob_all_filled

    def bob_turn(self, final_turn=False):
        """Handle Bob's turn to roll the dice and choose a formation. If it's the final turn, announce the winner."""
        rolled_values = [random.randint(1, 6) for _ in range(self.no_of_dices)]
        print(f"Bob rolled: {rolled_values}")
        self.bob_dice_values = rolled_values  
        self.update_bob_dice_display(rolled_values)  # Display Bob's dice roll

        # Get Bob's possible formations based on the roll
        possible_formations = self.bob.suggest_formation(rolled_values)

        # Ensure Bob chooses a valid unscored formation
        if possible_formations:
            chosen_formation = random.choice(possible_formations)
            if self.bob.scores.get(chosen_formation, 0) > 0:
                print(f"Bob's formation {chosen_formation} already filled, skipping.")
            else:
                score = sum(rolled_values)
                self.bob.scores[chosen_formation] = score
                print(f"Bob chose formation: {chosen_formation} with score {score}")

                # Update scores display
                self.scores_label.config(
                    text=f"Your Score: {sum(self.player.scores.values())}\nBob's Score: {sum(self.bob.scores.values())}")
                messagebox.showinfo("Bob's Turn", f"Bob chose formation: {chosen_formation}")

        if final_turn:
            # If this is Bob's final turn, calculate the final scores and announce the winner
            player_score = sum(self.player.scores.values())
            bob_score = sum(self.bob.scores.values())

            # Determine the winner
            if player_score > bob_score:
                winner = "You win!"
            elif bob_score > player_score:
                winner = "Bob wins!"
            else:
                winner = "It's a tie!"

            # Display the final scores and the winner
            messagebox.showinfo("Game Over", f"Final Scores:\nYou: {player_score}\nBob: {bob_score}\n{winner}")
            self.root.quit()  # Close the game after showing the result
        else:
            # If it's not the final turn, reset for the next round
            self.reset_dices()



    def select_formation_button_clicked(self):
        """Handle when the player clicks the 'Select Formation' button."""
        possible_formations = self.player.suggest_formation(self.kept_dice_values)
        self.choose_formation(possible_formations)

    def calculate_score_for_formation(self, formation):
        """Helper function to calculate score based on the formation and kept dice."""
        score = 0
        counts = Counter(self.kept_dice_values)
        counts_values = list(counts.values())

        if formation == "Yahtzee!":
            score = 50  # Yahtzee always scores 50 points
        elif formation == "Four of a Kind" and (4 in counts_values or 5 in counts_values):
            score = sum(self.kept_dice_values)
        elif formation == "Full House" and (3 in counts_values and 2 in counts_values):
            score = 25  # Full House scores 25 points
        elif formation == "Three of a Kind" and (3 in counts_values or 4 in counts_values or 5 in counts_values):
            score = sum(self.kept_dice_values)
        elif formation == "Large Straight" and (sorted(self.kept_dice_values) == [1, 2, 3, 4, 5] or sorted(self.kept_dice_values) == [2, 3, 4, 5, 6]):
            score = 40  # Large Straight scores 40 points
        elif formation == "Small Straight" and (set([1, 2, 3, 4]).issubset(self.kept_dice_values) or set([2, 3, 4, 5]).issubset(self.kept_dice_values) or set([3, 4, 5, 6]).issubset(self.kept_dice_values)):
            score = 30  # Small Straight scores 30 points
        elif formation == "Two Pairs" and counts_values.count(2) == 2:
            score = sum(self.kept_dice_values)
        elif formation == "One Pair" and 2 in counts_values:
            score = sum(self.kept_dice_values)

        return score


    def choose_formation(self, possible_formations):
        """Allow the player to choose a formation or assign 0 if the formation is already scored."""
        
        # Case 1: Valid formations exist, allow player to select them if not scored
        if possible_formations:
            self.formations_label.config(text="Choose a valid formation or assign 0 to another unscored one.")
            
            for widget in self.player_formations_frame.winfo_children():
                formation = widget.cget("text").split(":")[0]  # Get the formation name
                
                # If the formation is valid and not scored, allow selecting it for score calculation
                if formation in possible_formations and self.player.scores.get(formation) is None:
                    widget.config(state=tk.NORMAL, command=lambda f=formation: self.select_formation(f))
                
                # If the valid formation is already scored, enable assigning 0 to another unscored formation
                elif self.player.scores.get(formation) is None:
                    widget.config(state=tk.NORMAL, command=lambda f=formation: self.assign_zero(f))
                
                # Disable formations that are already scored
                else:
                    widget.config(state=tk.DISABLED)
        
        # Case 2: No valid formations, allow assigning 0 to any unscored formation
        else:
            self.formations_label.config(text="No valid formation available. Assign 0 to an unscored formation.")
            
            for widget in self.player_formations_frame.winfo_children():
                formation = widget.cget("text").split(":")[0]
                
                # Allow only unscored formations to be assigned 0
                if self.player.scores.get(formation) is None:
                    widget.config(state=tk.NORMAL, command=lambda f=formation: self.assign_zero(f))
                else:
                    widget.config(state=tk.DISABLED)  # Disable scored formations
        
        # Disable the roll and select buttons during formation selection
        self.roll_button.config(state=tk.DISABLED)
        self.select_formation_button.config(state=tk.DISABLED)


    def assign_zero(self, formation):
        """Assign 0 to the chosen formation if it hasn't been scored."""
        if self.player.scores.get(formation) is None:  # Only assign if the formation hasn't been scored yet
            self.player.scores[formation] = 0
            self.update_formations_display()
            messagebox.showinfo("Formation Assigned", f"Assigned 0 to {formation}.")  # Add message for confirmation
            self.end_turn()





    def select_formation(self, formation):
        """Assign the score to the chosen formation if it hasn't been scored yet."""
        if self.player.scores.get(formation) is None:  # Check if formation is not already scored
            score = self.calculate_score_for_formation(formation)  # Calculate score for the chosen formation
            self.player.scores[formation] = score
            self.update_formations_display()
            self.end_turn()





    def update_formations_display(self):
        """Update the display of formations and their scores."""
        for widget in self.player_formations_frame.winfo_children():
            widget.destroy()

        advanced_formations = ["Yahtzee!", "Four of a Kind", "Full House",
                            "Three of a Kind", "Large Straight", "Small Straight", "Two Pairs", "One Pair"]
        for formation in advanced_formations:
            score = self.player.scores.get(formation, "Not Scored")  # Display score or indicate unscored
            formation_button = tk.Button(self.player_formations_frame, text=f"{formation}: {score}", state=tk.DISABLED)
            formation_button.pack(anchor='w')



    def end_game(self):
        """Check final scores and declare the winner."""
        player_score = sum(self.player.scores.values())  # Calculate the total score for the player
        bob_score = sum(self.bob.scores.values())  # Calculate the total score for Bob

        print(f"Player Score: {player_score}, Bob Score: {bob_score}")

        # Determine the winner
        if player_score > bob_score:
            winner = "You win!"
        elif bob_score > player_score:
            winner = "Bob wins!"
        else:
            winner = "It's a tie!"

        # Display the final scores and the winner
        messagebox.showinfo("Game Over", f"Final Scores:\nYou: {player_score}\nBob: {bob_score}\n{winner}")
        print(f"Winner: {winner}")
        self.root.quit()  # Close the game after showing the result



    def display_possible_formations(self, possible_formations):
        if possible_formations:
            self.formations_label.config(text=f"Formations: {', '.join(possible_formations)}")
        else:
            self.formations_label.config(text="Formations: None")

if __name__ == "__main__":
    root = tk.Tk()
    game = YahtzeeGameGUI(root)
    root.mainloop()
