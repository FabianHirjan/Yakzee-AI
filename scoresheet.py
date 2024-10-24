from main import SMALL_FONT
from uielement import Label
from dice_logic import formations


# SCORESHEET_X = 600
# SCORESHEET_Y = 150
SCORESHEET_WIDTH = 180
SCORESHEET_HEIGHT = 300


class ScoreSheet:
    def __init__(self, SCORESHEET_X, SCORESHEET_Y):
        self.scores = {}
        self.SCORESHEET_X = SCORESHEET_X
        self.SCORESHEET_Y = SCORESHEET_Y

    def add_score(self, formation, score):
        self.scores[formation] = score

    def is_formation_used(self, formation):
        return formation in self.scores

    def get_labels(self):
        labels = []
        y_offset = 0
        for formation in formations:
            if formation in self.scores:
                score = self.scores[formation]
                label = Label(f"{formation}: {score}", (self.SCORESHEET_X, self.SCORESHEET_Y + y_offset),
                              SMALL_FONT, (128, 128, 128))  # gri
            else:
                label = Label(f"{formation}: ", (self.SCORESHEET_X, self.SCORESHEET_Y + y_offset),
                              SMALL_FONT, (255, 255, 255))  # alb
            labels.append(label)
            y_offset += 20
        return labels

    def get_total_score(self):
        return sum(self.scores.values())

    def clear_scores(self):
        self.scores = {}
