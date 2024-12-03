from collections import defaultdict
import pickle

def merge_q_tables(existing_q_table, new_q_table):
    for state, actions in new_q_table.items():
        if state not in existing_q_table:
            existing_q_table[state] = actions
        else:
            for action, value in actions.items():
                if action not in existing_q_table[state]:
                    existing_q_table[state][action] = value
                else:
                    existing_q_table[state][action] = max(existing_q_table[state][action], value)
    return existing_q_table

class YahtzeeAutoTrainer:
    def __init__(self):
        self.q_table_dice = defaultdict(default_q_values_dice)
        self.q_table_category = defaultdict(default_q_values_category)

    def load_q_tables(self, filename_dice, filename_category):
        try:
            with open(filename_dice, "rb") as f:
                existing_q_table_dice = pickle.load(f)
            print(f"Tabelul Q pentru zaruri a fost încărcat din: {filename_dice}")
            self.q_table_dice = merge_q_tables(existing_q_table_dice, self.q_table_dice)
        except FileNotFoundError:
            print(f"Fișierul {filename_dice} nu a fost găsit. AI-ul va învăța de la zero.")

        try:
            with open(filename_category, "rb") as f:
                existing_q_table_category = pickle.load(f)
            print(f"Tabelul Q pentru categorii a fost încărcat din: {filename_category}")
            self.q_table_category = merge_q_tables(existing_q_table_category, self.q_table_category)
        except FileNotFoundError:
            print(f"Fișierul {filename_category} nu a fost găsit. AI-ul va învăța de la zero.")

if __name__ == "__main__":
    trainer = YahtzeeAutoTrainer()
    trainer.load_q_tables("q_table_dice.pkl", "q_table_category.pkl")
    trainer.train(num_games=50000000, save_interval=100000, log_interval=10000)