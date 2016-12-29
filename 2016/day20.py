#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day20.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 20 puzzles for the advent of code (adventofcode.com/2016/day/20)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

MAX_IP = 4294967295
TEST_DATA = sorted([[5, 8], [0, 2], [4, 7]])

FNAME = os.path.join('data', 'day20.txt')
logger = logging.getLogger('day20')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return sorted(list(map(int, line.split('-'))) for line in f)


def q_1(data, maxip=MAX_IP):
    ipNow = 0
    for (low, high) in data:
        if ipNow < low:
            return ipNow
        else:
            ipNow = max(ipNow, high + 1)

    raise ValueError("terminated with no answer")


def test_q_1():
    assert q_1(TEST_DATA, 9) == 3


def q_2(data, maxip=MAX_IP):
    ipNow = 0
    allowed = 0
    for (low, high) in data:
        if ipNow < low:
            allowed += low - ipNow
            ipNow = high + 1
        else:
            ipNow = max(ipNow, high + 1)
    allowed += (maxip + 1 - ipNow)
    return allowed


def test_q_2():
    assert q_2(TEST_DATA, 9) == 2


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 20')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
