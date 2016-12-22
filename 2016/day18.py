#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day18.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 18 puzzles for the advent of code (adventofcode.com/2016/day/18)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

SAFE = '.'
TRAP = '^'

FNAME = os.path.join('data', 'day18.txt')
logger = logging.getLogger('day18')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def make_next_row(row):
    newRow = ''
    L = len(row)
    for i in range(L):
        l, c, r = row[(i - 1) % L], row[i], row[(i + 1) % L]

        if i == 0:
            l = SAFE
        elif i == L - 1:
            r = SAFE

        if (l == c != r) or (l != c == r):
            newchar = TRAP
        else:
            newchar = SAFE

        newRow += newchar
    return newRow


def q_1(data, numRows=40):
    rows = [data]
    while len(rows) < numRows:
        rows.append(make_next_row(rows[-1]))

    return sum(c == SAFE for row in rows for c in row)


def test_q_1():
    assert q_1('..^^.', numRows=3) == 6
    assert q_1('.^^.^.^^^^', numRows=10) == 38


def q_2(data):
    return q_1(data, numRows=400000)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 18')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
