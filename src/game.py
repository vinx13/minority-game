from random import randint

import pylab

from agent import Agent
from strategy import Strategy, StrategyTable


class MinorityGame(object):
    def __init__(self, n, m, s, t, grand_canonical, winning_decision_generator=None):
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
        self.decisions = []
        self.minority_decisions = []
        self.winning_decisions = []
        self.predictions = []
        self.winning_decision_generator = winning_decision_generator

        self.previous_series = randint(0, 2 ** m - 1)

        for agent in self.agents:
            for i in range(s):
                agent.add_strategy(Strategy(self.strategy_table.next_from_fss()))

    def next_step(self):
        self.collect_decisions()
        winning_decision = self.record_current_status()
        self.update_agents(winning_decision)
        self.update_previous_seires(winning_decision)

    def update_agents(self, winning_decision):
        # update score of all strategies of all agents
        for agent in self.agents:
            agent.update_strategies(self.previous_series, winning_decision)
        return winning_decision

    def record_current_status(self):
        self.winning_decisions.append(self.get_winning_decision())
        self.minority_decisions.append(self.get_minority_decision())
        self.predictions.append(self.get_majority_decision())
        return self.winning_decisions[-1]

    def collect_decisions(self):
        # collect decisions of all agents and append to self.decisions
        choices = [0, 0, 0]  # 0: skip this step if in GCMG, 1: choose side one 2: choose side zero
        for agent in self.agents:
            choices[agent.next_decision(self.previous_series)] += 1
        self.decisions.append((choices[-1], choices[1], choices[0]))

    def get_winning_decision(self):
        # generate next winning decision if the MG model is used as a predictor,
        # otherwise the winning decision is the minority decision
        if self.winning_decision_generator:
            return self.winning_decision_generator.next()
        return self.get_minority_decision()

    def get_minority_decision(self):
        # the minority decision of this step
        return 1 if self.decisions[-1][0] > self.decisions[-1][1] else -1

    def get_majority_decision(self):
        return -1 if self.decisions[-1][0] > self.decisions[-1][1] else 1

    def get_prediction(self):
        return self.get_majority_decision()

    def update_previous_seires(self, winning_decision):
        self.previous_series = self.previous_series << 1
        self.previous_series &= ~(1 << self.m)
        self.previous_series |= 1 if winning_decision == 1 else 0

    def run(self):
        for i in range(self.t):
            print i
            self.next_step()
        self.print_result()

    def print_strategies(self):
        for agent in self.agents:
            agent.print_strategies()

    def print_result(self):
        print self.decisions
        total = 0.0
        half_n = self.n / 2.0
        for result in self.decisions:
            total += (half_n - result[0]) ** 2 + (half_n - result[1]) ** 2
        total /= 2 * self.t
        total = total ** 0.5
        print "var=", total

    def plot(self):
        step = self.t / 300
        x = range(1, self.t + 1, step)
        pylab.ylim(0, 1)
        y = [self.decisions[i - 1][0] * 1.0 / self.n for i in x]
        pylab.plot(x, y)
        pylab.show()


if __name__ == '__main__':
    n = 100
    m = 10
    s = 4
    t = 10000
    mg = MinorityGame(n=n, m=m, s=s, t=t, grand_canonical=False)
    mg.run()
    mg.plot()
    mg.print_result()
