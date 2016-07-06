from random import randint

import pylab

from agent import Agent
from strategy import Strategy, StrategyTable


class MinorityGame(object):
    def __init__(self, n, m, s, t, grand_canonical):
        """
        :param n: number of agents
        :param m: limitation of memory
        :param s: number of strategies of each agent
        :param t: total steps to be run
        """
        self.n = n
        self.m = m
        self.s = s
        self.t = t
        self.agents = [Agent(s, grand_canonical) for i in range(n)]
        self.strategy_table = StrategyTable(m)
        self.results = []
        self.minority_decisions = []

        self.previous_series = randint(0, 2 ** m - 1)

        for agent in self.agents:
            for i in range(s):
                agent.add_strategy(Strategy(self.strategy_table.next_from_fss()))

    def next_step(self):
        choices = [0, 0, 0]  # 0: skip this step if in GCMG, 1: choose side one 2: choose side zero
        choice_one = choice_zero = choice_skip = 0
        for agent in self.agents:
            choices[agent.next_decision(self.previous_series)] += 1

        minority_decision = 1 if choices[1] < choices[-1] else -1
        self.minority_decisions.append(minority_decision)

        for agent in self.agents:
            agent.update_strategies(self.previous_series, minority_decision)
        self.update_previous_seires(minority_decision)

        self.results.append((choices[-1], choices[1], choices[0]))

    def update_previous_seires(self, winning_decision):
        self.previous_series = self.previous_series << 1
        self.previous_series &= ~(1 << self.m)
        self.previous_series |= 1 if winning_decision == 1 else 0

    def run(self):
        i = 0
        # for agent in self.agents:
        #    print "agent", i
        #    agent.print_strategies()
        #    i+=1
        for i in range(self.t):
            print i
            self.next_step()
        self.print_result()

    def print_result(self):
        print self.results
        total = 0.0
        half_n = self.n / 2.0
        for result in self.results:
            total += (half_n - result[0]) ** 2 + (half_n - result[1]) ** 2
        total /= 2 * self.t
        total = total ** 0.5
        print "var=", total

    def plot(self):
        step = self.t / 300
        x = range(1, self.t + 1, step)
        pylab.ylim(0, 1)
        y= [self.results[i-1][0]*1.0 / self.n for i in x]
        pylab.plot(x, y)
        pylab.show()

if __name__ == '__main__':
    mg = MinorityGame(n=100,m=8,s=4,t=1000, grand_canonical=True)
    mg.run()
    mg.plot()
    mg.print_result()
