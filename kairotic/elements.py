#  Common elements for games
import random
from collections import namedtuple


DECK_SIZE = 52
SUITS = ['D', 'H', 'S', 'C']
CARD_VALUES = [str(v) for v in range(2, 11)] + ['A', 'J', 'Q', 'K']


class Card(namedtuple('Card', ['value', 'suit'])):
    @property
    def baccarat_value(self):
        if self.value == 'A':
            return 1
        elif self.value in ('J', 'Q', 'K'):
            return 0
        else:
            return int(self.value)


class Die:
    def __init__(self, sides: int = 6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class Shoe:
    def __init__(self, num_decks: int, rem_at_cut: int=1.5 * DECK_SIZE, counts=[]):
        self.rem_at_cut = rem_at_cut
        self.num_decks = num_decks
        self.counts = []
        for count in counts:
            self.attach_count(count)
        self.reset()

    def attach_count(self, count):
        self.counts.append(count)
        count._n_decks = self.num_decks

    def reset(self):
        """Gathers all discards and shuffles full shoe"""
        self.remaining = [Card(v, s) for v in CARD_VALUES for s in SUITS] * self.num_decks
        self.shuffle_remaining()
        for count in self.counts:
            count.reset()

    def shuffle_remaining(self):
        """Assumes perfect shuffling"""
        random.shuffle(self.remaining)

    @property
    def cut_card_seen(self) -> bool:
        # +/- half deck on cut card
        return len(self.remaining) <= self.rem_at_cut

    def draw(self, face_down=False) -> Card:
        card = self.remaining.pop()
        if not face_down:
            for count in self.counts:
                count.update(card)
        return card


class Deck(Shoe):
    def __init__(self):
        super().__init__(1, 0)
