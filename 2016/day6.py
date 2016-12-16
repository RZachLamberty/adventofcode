#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day6.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 6 puzzles for the advent of code (adventofcode.com/2016/day/6)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TESTDAT = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""
FNAME = os.path.join('data', 'day6.txt')
logger = logging.getLogger('day6')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def q_1(data):
    return ''.join(
        collections.Counter(row[i] for row in data).most_common()[0][0]
        for i in range(len(data[0]))
    )


def test_q_1():
    assert q_1([
        row.strip() for row in TESTDAT.split('\n')
    ]) == 'easter'


def q_2(data):
    return ''.join(
        collections.Counter(row[i] for row in data).most_common()[-1][0]
        for i in range(len(data[0]))
    )


def test_q_2():
    assert q_2([
        row.strip() for row in TESTDAT.split('\n')
    ]) == 'advent'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 6')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
