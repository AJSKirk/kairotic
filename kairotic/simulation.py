from collections import Counter
from kairotic.counting import Count
from kairotic.elements import Shoe
from kairotic.games.base import Game
from tqdm import tqdm


def simulate_count(shoe: Shoe, n_cuts: int = 1000):
    seen = {count.name: Counter() for count in shoe.counts}
    print('Simulating {:,} shoes'.format(n_cuts))
    for _ in tqdm(range(n_cuts)):
        while not shoe.cut_card_seen:
            card = shoe.draw()
            for count in shoe.counts:
                seen[count.name].update([str(count.true_count)])

        shoe.reset()

    return seen


def calc_outcomes(game: Game, n_rounds: int = 1000000):
    wins = {bet: 0 for bet in game.payouts}
    evs = {bet: 0 for bet in game.bets}
    print('Simulating {:,} games'.format(n_rounds))
    for _ in tqdm(range(n_rounds)):
        outcome = game.play_round()
        for bet in game.bets:
            wins[bet] += (outcome[bet] > 0)
            if outcome[bet] > 0:
                evs[bet] += outcome[bet]
            else:
                evs[bet] -= 1

    # Normalize
    # evs = {bet: hits / n_rounds for bet, hits in evs.items()}
    probs = {bet: hits / n_rounds for bet, hits in wins.items()}

    return probs, evs
