from typing import NamedTuple
from kairotic.elements import Card


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card: Card):
        self.cards.append(card)
        return self.score

    @property
    def last_card(self):
        return self.cards[-1].baccarat_score

    @property
    def score(self):
        return sum(card.baccarat_value for card in self.cards)


class Baccarat:
    def __init__(self, shoe, player):
        self.shoe = shoe
        self.player = player

    def play_round(self):
        self.shoe.draw()  # Single burn
        player_hand = Hand()
        banker_hand = Hand()

        for _ in range(2):
            player_hand.add(self.shoe.draw)
            banker_hand.add(self.shoe.draw)

        if player_hand.score in (8, 9):
            if player_hand.score == banker_hand.score:
                return 'Tie'
            return 'Player'
        elif banker_hand.score in (8, 9):
            return 'Banker'

        if player_hand.score in (6, 7):  # Player stands pat
            if banker_hand.score <= 5:
                banker_hand.add(self.shoe.draw())
        else:  # Player draws
            if banker_hand.score <= 2:
                banker_hand.add(self.shoe.draw())
            elif banker_hand.score == 3 and player_hand.last_card != 8:
                banker_hand.add(self.shoe.draw())
            elif banker_hand.score == 4 and player_hand.last_card in range(2, 8):
                banker_hand.add(self.shoe.draw())
            elif banker_hand.score == 5 and player_hand.last_card in range(4, 8):
                banker_hand.add(self.shoe.draw())
            elif banker_hand.score == 6 and player_hand.last_card in range(6, 8):
                banker_hand.add(self.shoe.draw())

        if player_hand.score == banker_hand.score:
            return 'Tie'
        return 'Banker' if banker_hand.score > player_hand.score else 'Player'
