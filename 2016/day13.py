#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day13.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 13 puzzles for the advent of code (adventofcode.com/2016/day/13)

Usage:
    <usage>

"""

import collections
import functools
import os
import re

import scipy as sp

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = 1350
logger = logging.getLogger('day13')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


@functools.lru_cache(maxsize=None)
def is_wall(x, y, num):
    return collections.Counter(
        bin(num + ((x * x) + (3 * x) + (2 * x * y) + y + (y * y)))
    )['1'] % 2 == 1


def take_step(nowLocs, seenLocs, num):
    newLocs = set()
    for (x, y) in nowLocs:
        # up
        xNew, yNew = x + 1, y
        lNew = (xNew, yNew)
        if not ((lNew in seenLocs) or is_wall(xNew, yNew, num)):
            newLocs.add(lNew)

        # down
        xNew, yNew = x - 1, y
        lNew = (xNew, yNew)
        if not ((x == 0) or (lNew in seenLocs) or is_wall(xNew, yNew, num)):
            newLocs.add(lNew)

        # right
        xNew, yNew = x, y + 1
        lNew = (xNew, yNew)
        if not ((lNew in seenLocs) or is_wall(xNew, yNew, num)):
            newLocs.add(lNew)

        # left
        xNew, yNew = x, y - 1
        lNew = (xNew, yNew)
        if not ((y == 0) or (lNew in seenLocs) or is_wall(xNew, yNew, num)):
            newLocs.add(lNew)

    return newLocs


def q_1(data):
    start = (1, 1)
    seenLocs = {start}
    nowLocs = {start}

    i = 0
    while not (31, 39) in seenLocs:
        nowLocs = take_step(nowLocs, seenLocs, num=data)
        seenLocs.update(nowLocs)
        i += 1

    return i


def q_2(data):
    start = (1, 1)
    seenLocs = {start}
    nowLocs = {start}

    for i in range(50):
        nowLocs = take_step(nowLocs, seenLocs, num=data)
        seenLocs.update(nowLocs)

    return len(seenLocs)


def test_q_2():
    assert q_2(None) == None


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 13')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
