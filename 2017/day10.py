#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day10.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 10 puzzles for the advent of codec (adventofcode.com/2017/day/10)

Usage:
    <usage>

"""

import os

import eri.logging as logging

import utils


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day10.txt')
LOGGER = logging.getLogger('day10')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return 256, f.read().strip()


def q_1(data):
    skip = currpos = 0
    n, lengthstr = data
    # lengthstr to lengths
    lengths = [int(_) for _ in lengthstr.split(',')]
    l = list(range(n))
    l, currpos, skip = utils.apply_lengths(l, lengths, currpos, skip)
    return l[0] * l[1]


def test_q_1():
    assert q_1(
        (5, '3,4,1,5')
    ) == 12


def q_2(data):
    return utils.knot_hash(data)


def test_q_2():
    assert q_2((256, '')) == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert q_2((256, 'AoC 2017')) == '33efeb34ea91902bb2f59c9920caa6cd'
    assert q_2((256, '1,2,3')) == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert q_2((256, '1,2,4')) == '63960835bcdc130f0b66d7ff4f6a5a8e'


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 10')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
