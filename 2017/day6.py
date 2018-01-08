#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 6 puzzles for the advent of codec (adventofcode.com/2017/day/6)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day6.txt')
LOGGER = logging.getLogger('day6')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [int(_) for _ in f.read().strip().split('\t')]


def update_mem(mem):
    LOGGER.debug('before: {}'.format(mem))
    L = len(mem)
    i, m = max(enumerate(mem), key=lambda im: im[1])
    mem[i] = 0
    while m > 0:
        i += 1
        i %= L
        mem[i] += 1
        m -= 1
    LOGGER.debug('after: {}'.format(mem))


def q_1(mem):
    seen = set([tuple(mem)])
    L = len(mem)
    steps = 0

    while True:
        steps += 1
        update_mem(mem)
        tmem = tuple(mem)
        if tmem in seen:
            break
        else:
            seen.add(tmem)

    return steps


def test_q_1():
    assert q_1([0, 2, 7, 0]) == 5


def q_2(mem):
    seen = {tuple(mem): 0}
    L = len(mem)
    steps = 0

    while True:
        steps += 1
        update_mem(mem)
        tmem = tuple(mem)
        if tmem in seen:
            break
        else:
            seen[tmem] = steps

    return steps - seen[tmem]


def test_q_2():
    assert q_2([0, 2, 7, 0]) == 4


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 6')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
