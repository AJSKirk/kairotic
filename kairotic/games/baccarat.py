from typing import NamedTuple
from kairotic.elements import Card
from kairotic.games import Game


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card: Card):
        self.cards.append(card)
        return self.score

    @property
    def last_card(self):
        return self.cards[-1].baccarat_value

    @property
    def score(self):
        out = sum(card.baccarat_value for card in self.cards) % 10
        assert out < 10
        return out


class Baccarat(Game):
    def __init__(self, shoe):
        self.shoe = shoe
        # self.player = player
        self.bets = ['banker', 'player', 'tie']
        self.payouts = {'banker': .95, 'player': 1, 'tie': 8}

    def play_round(self) -> dict:
        if self.shoe.cut_card_seen:
            self.shoe.reset()

        outcome = {bet: 0 for bet in self.bets}
        self.shoe.draw()  # Single burn
        player_hand = Hand()
        banker_hand = Hand()

        for _ in range(2):
            player_hand.add(self.shoe.draw())
            banker_hand.add(self.shoe.draw())

        if player_hand.score in (8, 9) or banker_hand.score in (8, 9):
            if player_hand.score == banker_hand.score:
                outcome['tie'] = self.payouts['tie']
            elif banker_hand.score > player_hand.score:
                outcome['banker'] = self.payouts['banker']
            else:
                outcome['player'] = self.payouts['player']

        else:
            if player_hand.score in (6, 7):  # Player stands pat
                if banker_hand.score <= 5:
                    banker_hand.add(self.shoe.draw())
            else:  # Player draws
                player_hand.add(self.shoe.draw())
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
                outcome['tie'] = self.payouts['tie']
            elif banker_hand.score > player_hand.score:
                outcome['banker'] = self.payouts['banker']
            else:
                outcome['player'] = self.payouts['player']

        return outcome
