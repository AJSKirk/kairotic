#  Common elements for games
import random
from collections import namedtuple


DECK_SIZE = 52


Card = namedtuple('Card', ['value', 'suit'])


class Die:
    def __init__(self, sides: int = 6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class Shoe:
    suits = ['D', 'H', 'S', 'C']
    values = [str(v) for v in range(2, 11)] + ['A', 'J', 'Q', 'K']

    def __init__(self, num_decks: int, rem_at_cut=1.5):
        self.rem_at_cut = rem_at_cut
        self.num_decks = num_decks
        self.reset()

    def reset(self):
        """Gathers all discards and shuffles full shoe"""
        self.remaining = [Card(v, s) for v in self.values for s in self.suits] * self.num_decks
        self.shuffle_remaining()

    def shuffle_remaining(self):
        """Assumes perfect shuffling"""
        random.shuffle(self.remaining)


    @property
    def cut_card_seen(self) -> bool:
        # +/- half deck on cut card
        return len(self.remaining) <= self.rem_at_cut * DECK_SIZE

    def draw(self) -> (Card, bool):
        return self.remaining.pop(), self.cut_card_seen


class Deck(Shoe):
    def __init__(self):
        super().__init__(1, 0)
