#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day1.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 1 puzzles for the advent of code (adventofcode.com/2016/day/1)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

NESW = [
    [ 1,  0],
    [ 0,  1],
    [-1,  0],
    [ 0, -1],
]
FNAME = os.path.join('data', 'day1.txt')
logger = logging.getLogger('day1')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return parse_directions(f.read().strip())


def parse_directions(s):
    return [
        (direction[0], int(direction[1:]))
        for direction in s.split(', ')
        if direction
    ]


def q_1(directions):
    x = [0, 0]
    compDirIndex = 0

    for (rl, steps) in directions:
        compDirIndex = (compDirIndex + (1 if rl == 'R' else -1)) % 4
        x = [
            (xi + steps * di)
            for (xi, di) in zip(x, NESW[compDirIndex])
        ]
        logger.debug('x = {}'.format(x))

    return sum([abs(el) for el in x])


def test_q_1():
    assert q_1(parse_directions('R2, L3')) == 5
    assert q_1(parse_directions('R2, R2, R2')) == 2
    assert q_1(parse_directions('R5, L5, R5, R3')) == 12


def q_2(directions):
    x = [0, 0]
    compDirIndex = 0
    visitedSite = set((0, 0))

    for (rl, steps) in directions:
        compDirIndex = (compDirIndex + (1 if rl == 'R' else -1)) % 4

        # walk the path bruh
        for i in range(1, steps + 1):
            x = [(xi + di) for (xi, di) in zip(x, NESW[compDirIndex])]
            logger.debug('x = {}'.format(x))
            tx = tuple(x)
            if tx in visitedSite:
                return sum([abs(el) for el in x])
            else:
                visitedSite.add(tx)


def test_q_2():
    assert q_2(parse_directions('R8, R4, R4, R8')) == 4


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 1')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
