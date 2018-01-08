#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day11.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 11 puzzles for the advent of codec (adventofcode.com/2017/day/11)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day11.txt')
LOGGER = logging.getLogger('day11')
logging.configure()

Hexdir = collections.namedtuple('HexDirection', ['n', 'ne', 'nw'])


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def q_1(data):
    c = collections.Counter(data.split(','))
    effloc = Hexdir(
        c['n'] - c['s'],
        c['ne'] - c['sw'],
        c['nw'] - c['se'],
    )
    # in cube coords
    x = effloc.ne - effloc.nw
    y = effloc.n + effloc.nw
    z = -effloc.n + -effloc.ne

    return .5 * (abs(x) + abs(y) + abs(z))


def test_q_1():
    assert q_1('ne,ne,ne') == 3
    assert q_1('ne,ne,sw,sw') == 0
    assert q_1('ne,ne,s,s') == 2
    assert q_1('se,sw,se,sw,sw') == 3



def q_2(data):
    steps = data.split(',')
    x = y = z = maxdist = 0

    for step in steps:
        if step == 'n':
            delta = (0, 1, -1)
        elif step == 's':
            delta = (0, -1, 1)
        elif step == 'ne':
            delta = (1, 0, -1)
        elif step == 'sw':
            delta = (-1, 0, 1)
        elif step == 'nw':
            delta = (-1, 1, 0)
        elif step == 'se':
            delta = (1, -1, 0)

        deltax, deltay, deltaz = delta
        x += deltax
        y += deltay
        z += deltaz

        dist = .5 * (abs(x) + abs(y) + abs(z))

        maxdist = max(dist, maxdist)

    return maxdist


def test_q_2():
    assert True


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 11')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
