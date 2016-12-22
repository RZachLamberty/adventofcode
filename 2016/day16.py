#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day16.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 16 puzzles for the advent of code (adventofcode.com/2016/day/16)

Usage:
    <usage>

"""

import collections
import hashlib
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = ('10111011111001111', 272)
logger = logging.getLogger('day16')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


def dragonize(s):
    return s + '0' + ''.join(reversed(s.translate(str.maketrans({'0': '1', '1': '0'}))))


def checksum(s):
    ck = ''
    for i in range(0, len(s), 2):
        if s[i] == s[i + 1]:
            ck += '1'
        else:
            ck += '0'

    if len(ck) % 2 == 0:
        ck = checksum(ck)

    return ck


def q_1(data):
    state, disklen = data
    while len(state) < disklen:
        state = dragonize(state)

    ck = checksum(state[:disklen])

    return ck


def test_q_1():
    assert q_1(('10000', 20)) == '01100'


def q_2(data):
    state, olddisklen = load_data()
    return q_1((state, 35651584))


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 16')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
