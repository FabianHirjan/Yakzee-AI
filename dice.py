import random
import tkinter as tk


class Dice:
    def __init__(self, root, index):
        self.index = index  # Indexul zarului (de la 1 la 5)
        self.value = 1  # Valoarea inițială a zarului
        self.label = tk.Label(
            root, text=f"Dice {self.index}: {self.value}", font=("Helvetica", 18))
        self.label.pack()

    def roll(self):
        """Generează o valoare random între 1 și 6 și actualizează eticheta."""
        self.value = random.randint(1, 6)
        self.label.config(text=f"Dice {self.index}: {self.value}")

    def get_value(self):
        """Returnează valoarea curentă a zarului."""
        return self.value
