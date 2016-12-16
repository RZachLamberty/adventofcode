#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day14.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 14 puzzles for the advent of code (adventofcode.com/2016/day/14)

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

INPUT = 'ahsbgdzn'
logger = logging.getLogger('day14')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


def q_1(data):
    threeOf = collections.defaultdict(set)
    fiveOf = collections.defaultdict(set)
    hashes = set()

    i = 0
    while not len(hashes) == 64:
        re3 = re.search('(.)\\1\\1', hashlib.md5('{}{}'.format(data, i).encode()).hexdigest())
        if re3 is not None:
            threeOf[re3.groups()[0]].add(i)

        char5s = re.findall('(.)\\1\\1\\1\\1', hashlib.md5(('{}{}'.format(data, i).encode()).hexdigest))
        for char5 in char5s:
            fiveOf[char5].add(i)
            # if any of the previous 1k integers i are in char3 for this match
            # character, add that as a hash
            validHashes = threeOf[char5].intersection(range(max(0, i - 1000), i))
            hashes.update(validHashes)

        i += 1


def test_q_1():
    assert q_1(None) == None


def q_2(data):
    return None


def test_q_2():
    assert q_2(None) == None


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 14')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
