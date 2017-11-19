#!/usr/bin/env python3

import numpy as np
from collections import Counter

TICKS = 100000

l = 25
mu = 4


class State:
    def __init__(self, channel1, channel2, channel3):
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3

    def __str__(self):
        return 'P{}{}{}'.format(self.channel1, self.channel2, self.channel3)

    def __eq__(self, other):
        return str(self) == other


state = State(0, 0, 0)
cnt = Counter()
total_time = 0

event_time = lambda t: np.random.exponential(1 / t)


def transition(current_time):

    global state, total_time

    channel1_time = event_time(3 * mu)
    channel2_time = event_time(2 * mu)
    channel3_time = event_time(mu)
    channel23_time = event_time(3 * mu)
    channel12_time = event_time(5 * mu)
    channel13_time = event_time(4 * mu)
    channel123_time = event_time(6 * mu)

    prev_time = total_time
    prev_state = state

    if state == 'P000':
        state = State(1, 0, 0)
        total_time += current_time

    elif state == 'P100':
        if channel1_time < current_time:
            state = State(0, 0, 0)
            total_time += channel1_time
        else:
            state = State(1, 1, 0)
            total_time += current_time
    elif state == 'P110':
        if channel12_time < current_time:
            state = State(0, 0, 0)
            total_time += channel12_time
        elif channel1_time < current_time:
            state = State(1, 0, 0)
            total_time += channel1_time
        elif channel2_time < current_time:
            state = State(0, 1, 0)
            total_time += channel2_time
        else:
            state = State(1, 1, 1)
            total_time += current_time

    elif state == 'P010':

        if channel2_time < current_time:
            state = State(0, 0, 0)
            total_time += channel2_time
        else:
            state = State(1, 1, 0)
            total_time += current_time

    elif state == 'P111':

        if channel123_time < current_time:
            state = State(0, 0, 0)
            total_time += channel123_time
        elif channel12_time < current_time:
            state = State(0, 0, 1)
            total_time += channel12_time
        elif channel13_time < current_time:
            state = State(0, 1, 0)
            total_time += channel13_time
        elif channel23_time < current_time:
            state = State(1, 0, 0)
            total_time += channel23_time
        elif channel1_time < current_time:
            state = State(0, 1, 1)
            total_time += channel1_time
        elif channel2_time < current_time:
            state = State(1, 0, 1)
            total_time += channel2_time
        elif channel3_time < current_time:
            state = State(1, 1, 0)
            total_time += channel3_time

    elif state == 'P101':

        if channel13_time < current_time:
            state = State(0, 0, 0)
            total_time += channel13_time
        elif channel1_time < current_time:
            state = State(0, 0, 1)
            total_time += channel1_time
        elif channel3_time < current_time:
            state = State(1, 0, 0)
            total_time += channel3_time
        else:
            state = State(1, 1, 1)
            total_time += current_time

    elif state == 'P001':

        if channel3_time < current_time:
            state = State(0, 0, 0)
            total_time += channel3_time
        else:
            state = State(1, 0, 1)
            total_time += current_time

    elif state == 'P011':

        if channel23_time < current_time:
            state = State(0, 0, 0)
            total_time += channel23_time
        elif channel2_time < current_time:
            state = State(0, 0, 1)
            total_time += channel2_time
        elif channel3_time < current_time:
            state = State(0, 1, 0)
            total_time += channel3_time
        else:
            state = State(1, 1, 1)
            total_time += current_time

    cnt[str(prev_state)] += total_time - prev_time


for _ in range(TICKS):
    current_time = event_time(l)
    transition(current_time)

Px = sum([v for k, v in cnt.items() if str(k)[1] == '1']) / total_time
Py = sum([v for k, v in cnt.items() if str(k)[2] == '1']) / total_time
Pz = sum([v for k, v in cnt.items() if str(k)[3] == '1']) / total_time

Pdeny = cnt['P111'] / total_time
A = l * (1 - Pdeny)

for k, v in sorted(cnt.items(), key=str):
    print('{}: {}'.format(k, v / total_time))

print('Px: {}'.format(Px))
print('Py: {}'.format(Py))
print('Pz: {}'.format(Pz))
print('A: {}'.format(A))
