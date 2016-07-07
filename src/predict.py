from random import normalvariate

from game import MinorityGame


def main():
    t = 1000
    m = 4

    mg = MinorityGame(n=1, m=4, s=2 ** 16, t=t, grand_canonical=True,
                      winning_decision_generator=generate_random_series())
    mg.run()
    print mg.winning_decisions
    print mg.minority_decisions
    print mg.predictions
    print "correctness", calculate_correctness(mg.winning_decisions, mg.predictions)


def generate_random_series():
    l = [normalvariate(0, 1) for i in range(4)]
    while True:
        next_val = 0.7 * l[-1] - 0.4 * l[-2] - 0.2 * l[-3] - 0.1 * l[-4] + normalvariate(0, 1)
        l.append(next_val)
        yield 1 if next_val > 0 else -1


def calculate_correctness(a, b):
    correct = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            correct += 1
    return correct * 1.0 / len(a)


if __name__ == '__main__':
    main()
