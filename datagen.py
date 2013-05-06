import os
import pprint
import random
import sys

SPIN_UP = 1
SPIN_DOWN = 0

class DataGen(object):
    def __init__(self, mode="anti", size=300):
        if mode == "ferro":
            init = self.ferromanet_spins(size)
        elif mode == "anti":
            init = self.antiferromanet_spins(size)
        else:
            init = self.random_spins(size)
        self.data = self.init = init
        self.iterations = 0

    def next(self):
        self._recalc_data()
        self.iterations += 1
        return self.data

    def _recalc_data(self):
        # self.data = [random.randint(0,1) for r in xrange(10)]
        # if isinstance(self.data[0], list):
        #     self.data = [ i%2 for i in range(0,50) ]
        #     return self.data
        self.data = self.sequential(self.data[:], (lambda i=0, L=0, cL=0: 0.5))

    def sequential(self, spins, w0):
        original_spins = spins[:]
        while not self.is_uniform(spins) and original_spins == spins:
            random_index = random.randint(0, len(spins)-1)
            (spin_left, spin_right) = self.get_neigbours(random_index, spins)
            if spin_left == spin_right:
                spins[random_index] = spin_left
            elif w0(i=random_index, L=len(spins)) < random.random():
                spins[random_index] = self.flip_spin(spins[random_index])
        return spins

    def is_uniform(self, spins):
        return all(v is SPIN_UP for v in spins) or all(v is SPIN_DOWN for v in spins)

    def random_spins(self, size):
        # return [ random.randrange(0, 2) for _ in range(0, 15) ]
        return numpy.random.randint(2, size=size)

    def antiferromanet_spins(self, size):
        return [ i%2 for i in range(0,size) ]

    def ferromanet_spins(self, size):
        return [ SPIN_UP for i in range(0,size) ]

    def get_neigbours(self, index, lst):
        left  = (index-1) % len(lst)
        right = (index+1) % len(lst)
        return (lst[left], lst[right])

    def flip_spin(self, spin):
        if spin == SPIN_DOWN:
            return SPIN_UP
        else:
            return SPIN_DOWN

# print [SPIN_DOWN]*10
# spins = [0,1,0,1,0,1,0,0,0,0]
# dg = DataGen()
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
# print dg.sequential(spins, (lambda i=0, L=0, cL=0: 0.5))
