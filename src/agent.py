import random

class Agent(object):
    def __init__(self):
        self.strategies = []

    def next_decision(self, previous_series):
        best_index = get_best_strategy()
        return self.strategies[best_index].next_decision(previous_series)

    def get_best_strategy(self):
        self.strategies.sort(reverse=True)
        score = self.strategies[0].get_score()
        i = 1
        while i < len(self.strategies):
            if self.strategies[i].get_score != score:
                break
        return random.randint(0,i - 1)
