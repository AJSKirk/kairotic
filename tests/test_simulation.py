from kairotic.elements import Shoe
from kairotic.counting import HiLo
from kairotic.simulation import simulate_count

seen = simulate_count(HiLo(), Shoe(6), n_cuts=10000)
print(seen)