#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day17.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 17 puzzles for the advent of codec (adventofcode.com/2017/day/17)

Usage:
    <usage>

"""

import os

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day17.txt')
LOGGER = logging.getLogger('day17')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    return 344


def q_1(data):
    b = [0]
    currind = 0
    for toinsert in tqdm.trange(1, 2018):
        currind += data
        currind %= len(b)
        b = b[:currind + 1] + [toinsert] + b[currind + 1:]
        currind += 1
        currind %= len(b)
    return b[currind + 1]


def test_q_1():
    assert q_1(3) == 638


def q_2(data):
    b = [0]
    currind = 0
    n = None
    for toinsert in tqdm.trange(1, 50000001):
        currind += data
        currind %= toinsert
        currind += 1
        if currind == 1:
            n = toinsert
    return n


def test_q_2():
    assert True


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 17')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
