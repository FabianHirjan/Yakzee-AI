import random
import numpy as np
from collections import Counter, defaultdict
import pickle
import matplotlib.pyplot as plt


def default_q_values_dice():
    """Returnează valorile implicite pentru Q-Table pentru selecția zarurilor."""
    return np.zeros(32)  # 2^5 posibile selecții de zaruri


def default_q_values_category():
    """Returnează valorile implicite pentru Q-Table pentru alegerea categoriilor."""
    return np.zeros(7)  # 7 categorii din Yahtzee


class YahtzeeAutoTrainer:
    def __init__(self):
        self.dice = [0] * 5
        self.selected = [False] * 5
        self.categories = [
            "Three of a kind",
            "Four of a kind",
            "Full House",
            "Small Straight",
            "Large Straight",
            "Yahtzee",
            "Chance",
        ]
        self.scores = {category: None for category in self.categories}
        self.rolls_left = 3

        # Parametri Q-Learning
        self.q_table_dice = defaultdict(default_q_values_dice)
        self.q_table_category = defaultdict(default_q_values_category)
        self.epsilon = 1.0  # Inițial explorare completă
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.99995
        self.alpha = 0.5  # Rata de învățare
        self.gamma = 0.9  # Factorul de discount

    def reset_game(self):
        """Resetează starea jocului."""
        self.dice = [0] * 5
        self.selected = [False] * 5
        self.scores = {category: None for category in self.categories}
        self.rolls_left = 3

    def roll_dice(self):
        """Aruncă zarurile care nu sunt selectate."""
        for i in range(5):
            if not self.selected[i]:
                self.dice[i] = random.randint(1, 6)

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
        """Verifică dacă există o secvență dreaptă de zaruri."""
        unique = sorted(set(self.dice))
        for i in range(len(unique) - length + 1):
            if unique[i:i + length] == list(range(unique[i], unique[i] + length)):
                return True
        return False

    def get_state_dice(self):
        """Reprezentarea stării pentru selecția zarurilor."""
        grouped_dice = self.group_dice(self.dice)  # Obține frecvențele zarurilor
        return tuple(grouped_dice), self.rolls_left

    def get_state_category(self):
        """Reprezentarea stării pentru alegerea categoriei."""
        grouped_dice = self.group_dice(self.dice)  # Obține frecvențele zarurilor
        return tuple(grouped_dice)

    def group_dice(self, dice):
        """Reprezintă starea zarurilor ca un vector al frecvenței valorilor."""
        counts = Counter(dice)
        grouped_state = [counts[i] for i in range(1, 7)]
        return grouped_state

    def choose_action_dice(self, state):
        """Alege o selecție de zaruri bazată pe Q-Table pentru selecția zarurilor."""
        if np.random.rand() < self.epsilon:
            action = random.randint(0, 31)  # Explorare
        else:
            q_values = self.q_table_dice[state]
            action = np.argmax(q_values)  # Exploatare
        return action

    def action_to_dice_selection(self, action):
        """Mapează o acțiune la o selecție de zaruri."""
        binary = bin(action)[2:].zfill(5)
        return [bit == '1' for bit in binary]

    def choose_action_category(self, state):
        """Alege o categorie bazată pe Q-Table pentru alegerea categoriilor."""
        available_actions = [i for i, cat in enumerate(self.categories) if self.scores[cat] is None]
        if not available_actions:
            return None  # Nu sunt acțiuni disponibile

        if np.random.rand() < self.epsilon:
            action = random.choice(available_actions)  # Explorare
        else:
            q_values = self.q_table_category[state]
            filtered_q = [q_values[i] if i in available_actions else -np.inf for i in range(len(self.categories))]
            action = np.argmax(filtered_q)  # Exploatare
        return action

    def train(self, num_games=100000, save_interval=10000, log_interval=1000):
        """Antrenează AI-ul folosind Q-Learning."""
        game_scores = []  # Pentru a stoca scorurile fiecărui joc

        for game in range(1, num_games + 1):
            self.reset_game()
            game_score = 0
            dice_selection_history = []

            # Faza de aruncări
            while self.rolls_left > 0:
                state = self.get_state_dice()
                action_dice = self.choose_action_dice(state)
                selected = self.action_to_dice_selection(action_dice)
                self.selected = selected
                dice_selection_history.append((state, action_dice))

                self.roll_dice()
                next_state = self.get_state_dice()

                reward_dice = 0
                max_future_q_dice = max(self.q_table_dice[next_state]) if next_state in self.q_table_dice else 0
                old_value = self.q_table_dice[state][action_dice]
                self.q_table_dice[state][action_dice] += self.alpha * (
                    reward_dice + self.gamma * max_future_q_dice - old_value
                )

                self.rolls_left -= 1

            # Faza de alegere a categoriei
            state_category = self.get_state_category()
            action_category = self.choose_action_category(state_category)

            if action_category is not None:
                category = self.categories[action_category]
                reward_category = self.calculate_score(category)
                self.scores[category] = reward_category
                game_score += reward_category

                new_state_category = self.get_state_category()
                max_future_q_category = max(self.q_table_category[new_state_category]) if new_state_category in self.q_table_category else 0
                old_value_cat = self.q_table_category[state_category][action_category]
                self.q_table_category[state_category][action_category] += self.alpha * (
                    reward_category + self.gamma * max_future_q_category - old_value_cat
                )

                for past_state, past_action in dice_selection_history:
                    old_value_past = self.q_table_dice[past_state][past_action]
                    self.q_table_dice[past_state][past_action] += self.alpha * (
                        reward_category - old_value_past
                    )

            game_scores.append(game_score)  # Adaugă scorul total al jocului

            # Reducerea epsilon
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.epsilon_min, self.epsilon)

            if game % log_interval == 0:
                avg_score = sum(game_scores[-log_interval:]) / log_interval
                print(f"Joc {game}/{num_games}: Scor mediu {avg_score:.2f}")

            if game % save_interval == 0:
                self.save_q_tables(f"q_table_dice_{game}.pkl", f"q_table_category_{game}.pkl")

        self.save_q_tables("q_table_dice_final.pkl", "q_table_category_final.pkl")
        self.plot_rewards(game_scores)

    def plot_rewards(self, rewards):
        """Generează graficul recompenselor episodice."""
        plt.figure(figsize=(10, 5))
        plt.plot(rewards, label="Recompensă per episod")
        plt.xlabel("Episod")
        plt.ylabel("Recompensă")
        plt.title("Convergența algoritmului Q-Learning")
        plt.legend()
        plt.grid()
        plt.show()

    def save_q_tables(self, filename_dice="q_table_dice_final.pkl", filename_category="q_table_category_final.pkl"):
        with open(filename_dice, "wb") as f:
            pickle.dump(dict(self.q_table_dice), f)
        with open(filename_category, "wb") as f:
            pickle.dump(dict(self.q_table_category), f)


if __name__ == "__main__":
    trainer = YahtzeeAutoTrainer()
    # Antrenează AI-ul
    trainer.train(num_games=1000000, save_interval=10000, log_interval=1000)
