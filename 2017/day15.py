#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day15.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 15 puzzles for the advent of codec (adventofcode.com/2017/day/15)

Usage:
    <usage>

"""

import os

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day15.txt')
LOGGER = logging.getLogger('day15')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    return 783, 325


class Generator(object):
    def __init__(self, start, factor, criteriaval=None):
        self.val = start
        self.factor = factor
        self.criteriaval = criteriaval

    def __iter__(self):
        return self

    def _update(self):
        self.val *= self.factor
        self.val %= 2147483647

    def __next__(self):
        self._update()

        if self.criteriaval:
            while not (self.val % self.criteriaval == 0):
                self._update()

        return self.val


def q_1(data):
    a, b = data
    gena = Generator(a, 16807)
    genb = Generator(b, 48271)
    N = 2 ** 16
    matches = sum(
        (aval % N) == (bval % N)
        for (i, aval, bval) in zip(tqdm.trange(int(4e7)), gena, genb)
    )
    return matches


def test_q_1():
    assert q_1((65, 8921)) == 588


def q_2(data):
    a, b = data
    gena = Generator(a, 16807, 4)
    genb = Generator(b, 48271, 8)
    N = 2 ** 16
    matches = sum(
        (aval % N) == (bval % N)
        for (i, aval, bval) in zip(tqdm.trange(int(5e6)), gena, genb)
    )
    return matches


def test_q_2():
    assert q_2((65, 8921)) == 309


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 15')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
