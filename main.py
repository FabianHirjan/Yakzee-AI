import random
import numpy as np
from collections import Counter, defaultdict
import pickle
import matplotlib.pyplot as plt


def default_q_values_dice():
    
    return np.zeros(32)


def default_q_values_category():
    
    return np.zeros(7)


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

       
        self.q_table_dice = defaultdict(default_q_values_dice)  
        self.q_table_category = defaultdict(default_q_values_category)  
        self.epsilon = 1.0  
        self.epsilon_min = 0.1 
        self.epsilon_decay = 0.99995  
        self.alpha = 0.5  
        self.gamma = 0.9  

    def reset_game(self):
        
        self.dice = [0] * 5
        self.selected = [False] * 5
        self.scores = {category: None for category in self.categories}
        self.rolls_left = 3

    def roll_dice(self):
        
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
       
        unique = sorted(set(self.dice))
        for i in range(len(unique) - length + 1):
            if unique[i:i + length] == list(range(unique[i], unique[i] + length)):
                return True
        return False

    def get_state_dice(self):
        
        counts = Counter(self.dice)
        return tuple([counts[i] for i in range(1, 7)]), self.rolls_left

    def get_state_category(self):
       
        counts = Counter(self.dice)
        return tuple([counts[i] for i in range(1, 7)])

    def choose_action_dice(self, state):
       
        if np.random.rand() < self.epsilon:  
            return random.randint(0, 31)
        return np.argmax(self.q_table_dice[state])  

    def action_to_dice_selection(self, action):
        
        binary = bin(action)[2:].zfill(5)  
        return [bit == '1' for bit in binary]  

    def choose_action_category(self, state):
        
        available_actions = [i for i, cat in enumerate(self.categories) if self.scores[cat] is None]
        if not available_actions:
            return None
        if np.random.rand() < self.epsilon:  
            return random.choice(available_actions)
        q_values = self.q_table_category[state]
        
        return np.argmax([q_values[i] if i in available_actions else -np.inf for i in range(len(self.categories))])

    def estimate_reward(self):
        
        counts = Counter(self.dice)
        max_count = max(counts.values())

       
        if max_count == 5:
            return 100  
        elif max_count == 4:
            return 75  
        elif max_count == 3 and 2 in counts.values():
            return 50  
        elif self.has_straight(4):
            return 25
        elif self.has_straight(5):
            return 20  
        else:
            return sum(self.dice) / 5  

    def train(self, num_games=1000000, save_interval=10000, log_interval=1000):
        
        game_scores = []  

        for game in range(1, num_games + 1):
            self.reset_game() 
            dice_selection_history = []

            
            while self.rolls_left > 0:
                state = self.get_state_dice()
                action_dice = self.choose_action_dice(state)
                self.selected = self.action_to_dice_selection(action_dice)
                dice_selection_history.append((state, action_dice))

                self.roll_dice()
                next_state = self.get_state_dice()

               
                reward = self.estimate_reward()
                max_future_q = max(self.q_table_dice[next_state]) if next_state in self.q_table_dice else 0
                old_value = self.q_table_dice[state][action_dice]
                self.q_table_dice[state][action_dice] += self.alpha * (
                    reward + self.gamma * max_future_q - old_value
                )

                self.rolls_left -= 1

           
            state_category = self.get_state_category()
            action_category = self.choose_action_category(state_category)

            if action_category is not None:
                reward_category = self.calculate_score(self.categories[action_category])
                self.scores[self.categories[action_category]] = reward_category

                max_future_q = max(self.q_table_category[state_category]) if state_category in self.q_table_category else 0
                old_value = self.q_table_category[state_category][action_category]
                self.q_table_category[state_category][action_category] += self.alpha * (
                    reward_category + self.gamma * max_future_q - old_value
                )

                
                for past_state, past_action in dice_selection_history:
                    old_value = self.q_table_dice[past_state][past_action]
                    self.q_table_dice[past_state][past_action] += self.alpha * (
                        reward_category - old_value
                    )

            
            game_scores.append(sum(v for v in self.scores.values() if v is not None))

            
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            
            if game % log_interval == 0:
                avg_score = sum(game_scores[-log_interval:]) / log_interval
                print(f"Game {game}/{num_games}: Average score: {avg_score:.2f}")

            
            if game % save_interval == 0:
                self.save_q_tables(f"q_table_dice_{game}.pkl", f"q_table_category_{game}.pkl")

        self.save_q_tables("q_table_dice_final.pkl", "q_table_category_final.pkl")

    def save_q_tables(self, filename_dice="q_table_dice.pkl", filename_category="q_table_category.pkl"):
        
        with open(filename_dice, "wb") as f:
            pickle.dump(dict(self.q_table_dice), f)
        with open(filename_category, "wb") as f:
            pickle.dump(dict(self.q_table_category), f)


if __name__ == "__main__":
    trainer = YahtzeeAutoTrainer()
    trainer.train(num_games=1000000, save_interval=10000, log_interval=1000)
