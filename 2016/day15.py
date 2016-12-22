#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day15.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 15 puzzles for the advent of code (adventofcode.com/2016/day/15)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_INSTRUCTIONS = [
    'Disc #1 has 5 positions; at time=0, it is at position 4.',
    'Disc #2 has 2 positions; at time=0, it is at position 1.'
]
FNAME = os.path.join('data', 'day15.txt')
logger = logging.getLogger('day15')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def parse_instructions(instructions):
    return [
        list(map(
            int,
            re.match(
                'Disc #(\d) has (\d+) positions; at time=0, it is at position (\d+)',
                instruction
            ).groups()
        ))
        for instruction in instructions
    ]


def q_1(data):
    instructions = parse_instructions(data)

    i = 0
    while True:
        if all((n0 + i + delay) % n == 0 for (delay, n, n0) in instructions):
            break
        i += 1

    return i


def test_q_1():
    assert q_1(TEST_INSTRUCTIONS) == 5


def q_2(data):
    newdata = data + ['Disc #7 has 11 positions; at time=0, it is at position 0.']
    return q_1(newdata)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 15')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
