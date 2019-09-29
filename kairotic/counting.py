from kairotic.elements import DECK_SIZE, SUITS, CARD_VALUES


class Count:
    def __init__(self):
        self.cards_seen = 0
        self._n_decks = None

    @property
    def n_decks(self):
        if self._n_decks is None:
            raise UnboundLocalError("Count not attached to a Shoe")
        else:
            return self._n_decks

    def reset(self):
        self.cards_seen = 0

    def update(self, card):
        self.cards_seen += 1

    @property
    def half_decks_seen(self):
        return round(self.cards_seen / (DECK_SIZE / 2))

    @property
    def decks_rem(self):
        return max(self.n_decks - self.half_decks_seen / 2, .5)


class ScalarCount(Count):
    def __init__(self):
        super().__init__()
        self.running_count = 0

    def reset(self):
        super().reset()
        self.running_count = 0

    @property
    def true_count(self):
        return round(self.running_count / self.decks_rem)


class HiLo(ScalarCount):
    name = 'HiLo'

    def update(self, card):
        super().update(card)
        if card.value in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.value in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1


class VectorCount(Count):
    def __init__(self):
        super().__init__()
        self.running_count = dict()

    def reset(self):
        self.running_count = {key: 0 for key in self.running_count}

    @property
    def true_count(self):
        return {key: round(count / self.decks_rem) for key, count in self.running_count.items()}


class PerfectValueCount(VectorCount):
    name = 'Perfect Value Count'

    def __init__(self):
        super().__init__()
        self.running_count = {v: 0 for v in CARD_VALUES}

    def update(self, card):
        super().update(card)
        self.running_count[card.value] += 1
