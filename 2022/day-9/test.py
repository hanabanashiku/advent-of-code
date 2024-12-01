#!/usr/bin/env python

import sys
import numpy as np


def main() -> None:
    last = lambda in_list: in_list[-1]

    itxt = open("input.txt", mode='r').read().split()
    move = [(d, int(s)) for d, s in zip(itxt[::2], itxt[1::2])]
    dirs = {'R': np.array([1, 0]), 'L': np.array([-1, 0]),
            'U': np.array([0, 1]), 'D': np.array([0, -1])}

    head, tail = [np.array([0, 0])], [np.array([0, 0])]

    for d, s in move:
        for _ in range(s):
            loc = dirs.get(d) + last(head)
            dif = loc - last(tail)

            if abs(dif[0]) > 1 or abs(dif[1]) > 1:
                tail.append(last(head))

            head.append(loc)

    print(len(set([(i[0], i[1]) for i in tail])))


if __name__ == '__main__':
    sys.exit(main())