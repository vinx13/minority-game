import random


class Agent(object):
    def __init__(self, s, grand_canonical):
        self.strategies = []
        self.grand_canoical = grand_canonical

    def next_decision(self, previous_series):
        best_index = self.get_best_strategy()
        if self.strategies[best_index].get_score() < 0 and self.grand_canoical:
            return 0
        return self.strategies[best_index].next_decision(previous_series)

    def get_best_strategy(self):
        self.strategies.sort(key=lambda x: x.get_score(), reverse=True)
        last = self.strategies[0].get_score()
        score = self.strategies[0].get_score()

        i = 1
        while i < len(self.strategies):
            if self.strategies[i].get_score() != score:
                break
            i += 1
        return random.randint(0, i - 1)

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def update_strategies(self, previous_series, minority_decision):
        for strategy in self.strategies:
            strategy.update(previous_series, minority_decision)

    def print_strategies(self):
        i = 0
        for s in self.strategies:
            print "Strategy", i, str(s)
            i = i + 1
