#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 5 puzzles for the advent of codec (adventofcode.com/2017/day/5)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day5.txt')
LOGGER = logging.getLogger('day5')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def q_1(jumps):
    i = 0
    L = len(jumps)
    step = 0

    while 0 <= i < L:
        LOGGER.debug(jumps)
        jump = jumps[i]
        jumps[i] += 1
        i += jump
        step += 1

    LOGGER.debug(jumps)
    return step


def test_q_1():
    assert q_1([0, 3, 0, 1, -3]) == 5


def q_2(jumps):
    i = 0
    L = len(jumps)
    step = 0

    while 0 <= i < L:
        LOGGER.debug(jumps)
        jump = jumps[i]
        if jumps[i] >= 3:
            jumps[i] -= 1
        else:
            jumps[i] += 1
        i += jump
        step += 1

    LOGGER.debug(jumps)
    return step


def test_q_2():
    assert q_2([0, 3, 0, 1, -3]) == 10


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 5')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))

    # if this ain't the dirtiest goddamn shit...
    data = load_data()
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
