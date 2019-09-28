from kairotic.elements import Shoe
from kairotic.counting import HiLo
from kairotic.simulation import *
import kairotic.games


seen = simulate_count(HiLo(), Shoe(6), n_cuts=1000)
print(seen)

baccarat = kairotic.games.Baccarat(Shoe(8, 8))
probs, evs = calc_outcomes(baccarat)
assert abs(probs['banker'] + probs['player'] + probs['tie'] - 1) <= .001
print(probs)
print(evs)
