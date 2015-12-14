#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day14.py
Author: zlamberty
Created: 2015-12-09

Description:
    day 14 puzzles for the advent of code (adventofcode.com/day/14)

Usage:
    <usage>

"""

import os
import re

from collections import Counter


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day14.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_rspeeds(fname=FNAME):
    rspeeds = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            r, v, t, rest = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.', line.strip()).groups()
            rspeeds[r] = (int(v), int(t), int(rest))

    return rspeeds


def dist_at_t(v, t, rest, totalT):
    tremaining = totalT
    d = 0
    while tremaining > 0:
        d += v * min(tremaining, t)
        tremaining -= (t + rest)
    return d


def q_1(rspeeds):
    return max(dist_at_t(v, t, rest, 2503) for (v, t, rest) in rspeeds.values())


def q_2(rspeeds):
    return Counter(
        max(
            rspeeds,
            key=lambda r: dist_at_t(
                rspeeds[r][0], rspeeds[r][1], rspeeds[r][2], i
            )
        ) for i in range(1, 2504)
    )


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 14 ########################################################"
    rspeeds = load_rspeeds()
    print "\tquestion 1 answer: {}".format(q_1(rspeeds))
    print "\tquestion 2 answer: {}".format(q_2(rspeeds))
