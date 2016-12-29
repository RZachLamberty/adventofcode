#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day22.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 22 puzzles for the advent of code (adventofcode.com/2016/day/22)

Usage:
    <usage>

"""

import itertools
import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day22.txt')
logger = logging.getLogger('day22')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        f.readline()
        f.readline()
        return [
            list(
                map(
                    int,
                    re.match(
                        '.*\-x(\d+)\-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%',
                        line.strip()
                    ).groups()
                )
            )
            for line in f
        ]


def is_viable(n0, n1):
    return n0['used'] and n0['used'] <= n1['avail']


def q_1(data):
    nodes = [
        dict(zip(['ix', 'iy', 'size', 'used', 'avail', 'use'], row))
        for row in data
    ]

    return sum(is_viable(n0, n1) for (n0, n1) in itertools.permutations(nodes, 2))


def test_q_1():
    assert q_1(TEST_DATA) == 'decab'


def q_2(data, target='fbgdceah'):
    answers = []
    s, instructions = data
    for perm in itertools.permutations(target):
        s = ''.join(perm)
        logger.info('trying string {}'.format(s))
        if q_1((s, instructions)) == target:
            answers.append(s)
    return sorted(answers)[0]


def test_q_2():
    assert q_2(TEST_DATA, 'decab') == 'abcde'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 22')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
