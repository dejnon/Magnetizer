#!/usr/bin/python

S = {-1,1,-1,1,1,-1,-1,-1}

def algorithm1(S,W0):
    while (True):
        i = randn(1, len(S))
        if ( S[i-1] == S[i+1] ):
            S[i] = S[i-1]
        elif ( W0(i) > randn(0,1) ):
            # bigger W0 -> greater chance for spin change
            S[i] = -S[i]

