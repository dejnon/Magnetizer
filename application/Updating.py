from random import randint
from random import random as randfloat
import random

SPIN_UP = 1
SPIN_DOWN = 0

class Updating():
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta


    def random_spins(size):
      return [ random.randrange(0, 2) for _ in range(0, 15) ]

    def antiferromanet_spins(size):
      return [ i%2 for i in range(0,size) ]

    # a = [6,7,9,4]
    # print getNeigbours(a,3) == (9,6)
    # print getNeigbours(a,0) == (4,7)
    # print getNeigbours(a,1) == (6,9)
    def get_neigbours(index, lst):
      left  = (index-1) % len(lst)
      right = (index+1) % len(lst)
      return (lst[left], lst[right])

    def flip_spin(spin):
      if spin == SPIN_DOWN:
        return SPIN_UP
      else:
        return SPIN_DOWN

    def prints(value):
      print(value)

    # SEQUENTIAL UPDATING
    # For random spin flip choosen spin with propability w0 if neighbours differ
    # Note: bigger W0 -> greater chance for spin change
    def sequential(spins, w0, timeout, iteration_callback=prints):
      while timeout:
        random_index = randint(0, len(spins)-1)
        (spin_left, spin_right) = get_neigbours(random_index, spins)
        if spin_left == spin_right:
          spins[random_index] = spin_left
        elif w0(i=random_index, L=len(spins)) < randfloat():
          spins[random_index] = flip_spin(S[random_index])
        iteration_callback(spins)
        timeout -= 1
      return spins

    # def w0(i=0, L=0, cL=0): return 0.5
    def w0(i=0, L=0, cL=0): return ((1./L)*i)
    # S = random_spins(100)
    S = antiferromanet_spins(30)
    # sequential(S, w0, 4000)












    # C-SEQUENTIAL UPDATING
    # With propability w0 flip cL consecutive spins
    # Note: consecutive spins are always flipped
    # Upgrade: consecutive spins could be flipped only if their spin is antiparallel
    def csequential(spins, w0, cL, timeout, iteration_callback=prints):
      cL_spins = int(len(spins)*cL) # for L = 12 and cL = 0.5 then cL_spins = 6
      while timeout:
        random_index = randint(0, len(spins)-1)
        if w0(cL=cL, L=len(spins), i=random_index) > randfloat():
          for i in xrange(random_index, (random_index+cL_spins)):
            i = i % len(spins) # spins on the circle
            spins[i] = flip_spin(spins[i])
        iteration_callback(spins)
        timeout -= 1
      return spins


    # def w0(i=0, L=0, cL=0): return 0.5
    # S = antiferromanet_spins(30)
    # csequential(S, w0, 0.1, 4000)


    # SYNCHRONOUS UPDATING
    # Iterate over spins. With propability w0 flip the spin
    def synchronous(spins, w0, timeout, iteration_callback=prints):
      while timeout:
        spins_copy = list(spins)
        for index in xrange(0,len(spins)):
          random_index = randint(0, len(spins)-1)
          (spin_left, spin_right) = getNeigbours(random_index, spins)
        if spin_left == spin_right:
          S[random_index] = spin_left
        elif w0(i=random_index, L=len(spins)) < randfloat():
          S[random_index] = flip_spin(S[random_index])
        iteration_callback(spins)
        timeout -= 1
      return spins



