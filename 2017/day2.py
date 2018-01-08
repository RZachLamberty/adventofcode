#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day2.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 2 puzzles for the advent of codec (adventofcode.com/2017/day/2)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_1 = """5 1 9 5
7 5 3
2 4 6 8"""
TEST_2 = """5 9 2 8
9 4 7 3
3 8 6 5"""
FNAME = os.path.join('data', 'day2.txt')
LOGGER = logging.getLogger('day2')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return parse_data(f.read().replace('\t', ' '))


def parse_data(s):
    return [
        [
            int(n)
            for n in line.strip().split(' ')
            if n
        ]
        for line in s.strip().split('\n')
    ]


def q_1(data):
    return sum(
        (max(row) - min(row))
        for row in data
    )


def test_q_1():
    assert q_1(parse_data(TEST_1)) == 18


def q_2(data):
    s = 0
    for row in data:
        rowbreak = False
        for (i, r0) in enumerate(row[:-1]):
            for (j, r1) in enumerate(row[i + 1:]):
                rmin, rmax = sorted([r0, r1])
                if rmax % rmin == 0:
                    s += rmax / rmin
                    rowbreak = True
                    break
            if rowbreak:
                break
    return s


def test_q_2():
    assert q_2(parse_data(TEST_2)) == 9


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 2')
    data = load_data()
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
