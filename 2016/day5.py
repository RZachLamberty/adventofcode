#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 5 puzzles for the advent of code (adventofcode.com/2016/day/5)

Usage:
    <usage>

"""

import hashlib

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = 'wtnhxymk'
logger = logging.getLogger('day5')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


def q_1(inp):
    n = 0
    pw = ''
    while len(pw) < 8:
        h = hashlib.md5('{}{}'.format(inp, n).encode()).hexdigest()
        if h[:5] == '00000':
            pw += h[5]
            logger.debug('pw updated; pw = {}'.format(pw))
        n += 1
    return pw


def test_q_1():
    assert q_1('abc') == '18f47a30'


def q_2(inp):
    n = 0
    pw = [None] * 8
    while not all(pw):
        h = hashlib.md5('{}{}'.format(inp, n).encode()).hexdigest()
        if h[:5] == '00000':
            try:
                pos = int(h[5])
            except ValueError:
                pos = None
            if (pos is not None) and (0 <= pos < 8) and pw[pos] is None:
                # will keep previous versions but not None-s
                pw[pos] = h[6]
                logger.debug('pw updated; pw = {}'.format(pw))
        n += 1
    return ''.join(pw)


def test_q_2():
    assert q_2('abc') == '05ace8e3'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 5')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
