from itertools import product
from random import randint


class Strategy(object):
    def __init__(self, strategy_map):
        self.score = 0
        self.strategy_map = strategy_map

    def update(self, previous_series, minority_decision):
        if self.next_decision(previous_series) == minority_decision:
            self.score += 1
        else:
            self.score -= 1

    def get_score(self):
        return self.score

    def next_decision(self, previous_series):
        return self.strategy_map[previous_series]

    def __str__(self):
        return str(self.strategy_map) + " score = " + str(self.score)


class StrategyTable:
    def __init__(self, m):
        self.m = m
        self.fss_generator = self.generate_fss()
        self.rss_generator = self.generate_rss()

    def generate_fss(self):
        total_bits = 2 ** self.m
        for tup in product([0, 1], repeat=total_bits):
            yield list(tup)

    def next_from_fss(self):
        total_bits = 2 ** self.m
        choices = [-1, 1]
        return [choices[randint(0, 1)] for i in range(total_bits)]

    def generate_rss(self):
        pass
