from random import normalvariate

import pylab

from game import MinorityGame


def main():
    t = 3000

    m = 4
    s = 2
    x = []
    y = []
    n = 1
    while s < 3000:
        x.append(s)
        mg = MinorityGame(n=n, m=m, s=s, t=t, grand_canonical=True,
                          winning_decision_generator=stock_series_generator())
        mg.run()
        print "winning decisions"
        print mg.winning_decisions
        # print "minority decisions\n"
        # print mg.minority_decisions
        print "predictions \n"
        print mg.predictions
        correctness = calculate_correctness(mg.winning_decisions, mg.predictions)
        y.append(correctness)
        print "correctness", correctness

        s *= 2
    pylab.plot(x, y)
    pylab.show()


def random_series_generator():
    l = [normalvariate(0, 1) for i in range(3)]
    while True:
        next_val = 0.7 * l[-1] - 0.5 * l[-2] - 0.2 * l[-3] + normalvariate(0, 1)
        l.append(next_val)
        # next_val = normalvariate(0,1)
        yield 1 if next_val > 0 else -1


def stock_series_generator():
    f = open("../data/000001.ss")
    f.readline()
    l = []
    for line in f.readlines():
        l.append(line.split(',')[-1])
    l.reverse()
    l = l[-3001:]
    for i in range(3000):
        t = 1 if l[i + 1] > l[i] else -1
        yield t


def calculate_correctness(a, b):
    correct = 0
    for i in range(len(a) - 100, len(a)):
        if a[i] == b[i]:
            correct += 1
    return correct * 1.0 / 100


if __name__ == '__main__':
    main()
