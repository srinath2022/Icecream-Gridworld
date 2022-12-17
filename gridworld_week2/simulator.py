from random import random


class GridSim:
    def __init__(self, s, a, p, so):
        self.s = s
        self.a = a
        self.p = p
        self.state = so

    def check_sim(self):
        if len(self.p) != len(self.s) or len(self.p[0]) != len(self.a) or len(self.p[0][0]) != len(self.s):
            print('Not valid S, A, or P')

    def next_state(self, action):
        pnstate = self.p[self.s.index(self.state)][self.a.index(action)]
        print(pnstate)

        pvalue = random()
        nstate = []
        for i in range(len(pnstate)):
            if pnstate[i] == 0:
                continue
            else:
                pvalue -= pnstate[i]
                if pvalue <= 0:
                    nstate = self.s[i]
        return nstate
