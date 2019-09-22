from kairotic.elements import DECK_SIZE


class Count:
    def __init__(self, n_decks: int = 6, start=0):
        self.running_count = start
        self.cards_seen = 0
        self.n_decks = n_decks

    def update(self, card):
        raise NotImplementedError

    def reset(self):
        self.count = 0

    @property
    def half_decks_seen(self):
        return (DECK_SIZE / 2) * round(self.cards_seen / (DECK_SIZE / 2))

    @property
    def true_count(self):
        decks_rem = self.n_decks - self.half_decks_seen / 2
        return round(self.running_count / decks_rem)


class HiLo(Count):
    def update(self, card):
        if card.value in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.value in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1
        return self.true_count
