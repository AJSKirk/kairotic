from collections import Counter
from kairotic.counting import Count
from kairotic.elements import Shoe
from tqdm import tqdm


def simulate_count(count: Count, shoe: Shoe, n_cuts=1000):
    seen = Counter()
    print('Simulating {:,} shoes'.format(n_cuts))
    for _ in tqdm(range(n_cuts)):
        while not shoe.cut_card_seen:
            card, _ = shoe.draw()
            seen.update([count.update(card)])

        shoe.reset()
        count.reset()

    return seen
