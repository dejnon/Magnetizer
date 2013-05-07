import os
import pprint
import random
import sys
import numpy

SPIN_UP = 1
SPIN_DOWN = 0

UPDATING_SEQUENTIAL = 'sequential'
UPDATING_SYNCHRONOUS = 'synchronous'
UPDATING_CSEQUENTIAL = 'csequential'

SPINS_FERROMANET = 0
SPINS_ANTIFERROMAGNET = 1
SPINS_RANDOM = 2

BOUNDARIES_CYCLIC = 0
BOUNDARIES_SHARP = 1

class DataGen(object):
    # update = sequential
    # eq = "x**2"
    # func = eval("lambda x: " + eq)

    def __init__(self, mode=SPINS_ANTIFERROMAGNET, size=300):
        self.data = self.init = self.ferromanet_spins(size)
        self.interations_left = 100
        self.boundaries = BOUNDARIES_CYCLIC
        self.running = False
        self.mode = 0
        self.size = size
        self.cL = 1/size
        self.w0 = (lambda i=0, L=0, cL=0: 0.5)
        self.updating = UPDATING_SEQUENTIAL

    def initialise(self):
        self.running = False
        self.data = self.ferromanet_spins(self.size)
        return self.data

    def next(self):
        if not self.running:
            self.running = True
            if self.mode == SPINS_FERROMANET:
                self.data = self.ferromanet_spins(self.size)
            elif self.mode == SPINS_ANTIFERROMAGNET:
                self.data = self.antiferromanet_spins(self.size)
            else:
                self.data = self.random_spins(self.size)
        if self.interations_left > 0:
            self.interations_left -= 1
            self._recalc_data()
        return self.data

    def _recalc_data(self):
        if self.updating == UPDATING_SEQUENTIAL:
            self.data = self.sequential(self.data[:], self.w0)
        elif self.updating == UPDATING_CSEQUENTIAL:
            self.data = self.csequential(self.data[:], self.w0, self.cL)
        else: # synchronous
            self.data = self.synchronous(self.data[:], self.w0)

    def sequential(self, spins, w0):
        original_spins = spins[:]
        while (not self.is_uniform(spins)) and (original_spins == spins):
            random_index = random.randint(0, len(spins)-1)
            (spin_left, spin_right) = self.get_neigbours(random_index, spins)
            if spin_left == spin_right:
                spins[random_index] = spin_left
            elif w0(i=random_index, L=len(spins), cL=(1/len(spins))) < random.random():
                spins[random_index] = self.flip_spin(spins[random_index])
        return spins

    def csequential(spins, w0, cL):
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

    def synchronous(spins, w0):
        while timeout:
            spins_copy = list(spins)
            for index in xrange(0,len(spins)):
                random_index = randint(0, len(spins)-1)
                (spin_left, spin_right) = getNeigbours(random_index, spins)
                if spin_left == spin_right:
                    S[random_index] = spin_left
                elif w0(i=random_index, L=len(spins)) < randfloat():
                    S[random_index] = flip_spin(S[random_index])
            timeout -= 1
        return spins

    def is_uniform(self, spins):
        return all(v is SPIN_UP for v in spins) or all(v is SPIN_DOWN for v in spins)

    def random_spins(self, size):
        return [ random.randrange(0, 2) for _ in range(0, size) ]
        # return numpy.random.randint(2, size=size)

    def antiferromanet_spins(self, size):
        return [ i%2 for i in range(0,size) ]

    def ferromanet_spins(self, size):
        return [ SPIN_UP for i in range(0,size) ]

    def get_neigbours(self, index, lst):
        if self.boundaries == BOUNDARIES_CYCLIC:
            left  = (index-1) % len(lst)
            right = (index+1) % len(lst)
        else: # BOUNDARIES_SHARP
            left  = (index-1)
            right = (index+1)
            if index == 0:          # 1st element
                left = index
            if index == len(lst):   # last element
                right = len(lst)
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
