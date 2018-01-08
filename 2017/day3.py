#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day3.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 3 puzzles for the advent of codec (adventofcode.com/2017/day/3)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day3.txt')
LOGGER = logging.getLogger('day3')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    return 325489


def q_1(n):
    if n == 1:
        return 0

    # which shell?
    shell = 1
    while n > (2 * shell + 1) ** 2:
        shell += 1

    # how wide is this shell, or more importantly, how many elements are in each
    # side?
    num_per_side = 2 * shell + 1
    shell_start = (num_per_side - 2) ** 2

    # this range of numbers between successive odd-number squares has 8n
    # elements in it. they are in 4 groups of 2n elements (per side)
    transverse = (n - shell_start - 1) % (num_per_side - 1) + 1

    # to get to a corner you would take (shell, shell) steps. wlog assume all up
    # and left, so positive. if the destination is not on the corner, you've
    # walked farther than you needed to. walk it back some number of steps
    # (subtract). "going negative" here is just crossing 0, so abs after
    # subtracting

    return shell + abs(shell - transverse)


def test_q_1():
    assert q_1(1) == 0
    assert q_1(12) == 3
    assert q_1(23) == 2
    assert q_1(1024) == 31


def sum_neighbors(x, i, j):
    s = 0
    for i1 in range(i - 1, i + 2):
        for j1 in range(j - 1, j + 2):
            if i1 == i and j1 == j:
                pass
            else:
                try:
                    s += x[i1, j1]
                except KeyError:
                    pass
    return s


def q_2(data):
    x = {(0, 0): 1}

    i = j = 0

    while True:
        # start new shell
        j += 1
        shellval = j
        x[i, j] = sum_neighbors(x, i, j)
        if x[i, j] > data:
            return x[i, j]

        # go "down"
        while i > -shellval:
            i -= 1
            x[i, j] = sum_neighbors(x, i, j)
            if x[i, j] > data:
                return x[i, j]

        # go "left"
        while j > -shellval:
            j -= 1
            x[i, j] = sum_neighbors(x, i, j)
            if x[i, j] > data:
                return x[i, j]

        # go "up"
        while i < shellval:
            i += 1
            x[i, j] = sum_neighbors(x, i, j)
            if x[i, j] > data:
                return x[i, j]

        # go "right"
        while j < shellval:
            j += 1
            x[i, j] = sum_neighbors(x, i, j)
            if x[i, j] > data:
                return x[i, j]


def test_q_2():
    assert q_2(24) == 25
    assert q_2(100) == 122


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 3')
    data = load_data()
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
