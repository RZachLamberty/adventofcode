#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day2.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 2 puzzles for the advent of code (adventofcode.com/2016/day/2)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day2.txt')
logger = logging.getLogger('day2')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def q_1(instructions):
    i = 5
    pw = ''
    for instruction in instructions:
        for dirchar in instruction:
            if dirchar == 'U':
                i = i - 3 if i > 3 else i
            elif dirchar == 'D':
                i = i + 3 if i < 7 else i
            elif dirchar == 'L':
                i = i - 1 if (i % 3) != 1 else i
            else:
                i = i + 1 if (i % 3) != 0 else i
            logger.debug("{} --> {}".format(dirchar, i))
        pw += str(i)
    logger.debug(pw)
    return pw


def test_q_1():
    assert q_1(['ULL', 'RRDDD', 'LURDL', 'UUUUD']) == '1985'


def q_2(instructions):
    i, j = [2, 0]
    kp = [
        [None, None, 1, None, None],
        [None, 2, 3, 4, None],
        [5, 6, 7, 8, 9],
        [None, 'A', 'B', 'C', None],
        [None, None, 'D', None, None]
    ]
    pw = ''
    for instruction in instructions:
        for dirchar in instruction:
            if dirchar == 'U' and i != 0:
                newI, newJ = i - 1, j
            elif dirchar == 'D' and i != 4:
                newI, newJ = i + 1, j
            elif dirchar == 'L' and j != 0:
                newI, newJ = i, j - 1
            elif dirchar == 'R' and j != 4:
                newI, newJ = i, j + 1
            else:
                newI, newJ = i, j
            newval = kp[newI][newJ]
            if newval is not None:
                i, j = newI, newJ
            logger.debug("{} --> {}".format(dirchar, kp[i][j]))
        if newval is not None:
            pw += str(newval)
        logger.debug(pw)
    return pw


def test_q_2():
    assert q_2(['ULL', 'RRDDD', 'LURDL', 'UUUUD']) == '5DB3'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 2')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
