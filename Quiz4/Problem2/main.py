import random
from collections import defaultdict
import itertools


def naive_shuffle(deck):
    cards = deck[:]
    for i in range(len(cards)):
        n = random.randint(0, len(cards) - 1)
        cards[i], cards[n] = cards[n], cards[i]
    return tuple(cards)


def fisher_yates_shuffle(deck):
    cards = deck[:]
    for i in range(len(cards) - 1, 0, -1):
        n = random.randint(0, i)
        cards[i], cards[n] = cards[n], cards[i]
    return tuple(cards)


def run_simulation(shuffle_func, times=1000000):
    deck = [1, 2, 3, 4]
    counts = defaultdict(int)
    for _ in range(times):
        shuffled = shuffle_func(deck)
        counts[shuffled] += 1
    return counts


def print_distribution(title, counts):
    print(title)
    for combo in sorted(counts.keys()):
        print(f"{list(combo)}: {counts[combo]}")


if __name__ == "__main__":
    naive_counts = run_simulation(naive_shuffle)
    fisher_counts = run_simulation(fisher_yates_shuffle)

    print_distribution("Naive Shuffle:", naive_counts)
    print()
    print_distribution("Fisher-Yates Shuffle:", fisher_counts)
