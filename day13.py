#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day13.py
Author: zlamberty
Created: 2015-12-09

Description:
    day 13 puzzles for the advent of code (adventofcode.com/day/13)

Usage:
    <usage>

"""

import itertools
import os
import re

from collections import defaultdict


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day13.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_happyscores(fname=FNAME):
    happyscores = defaultdict(dict)
    with open(fname, 'r') as f:
        for line in f.readlines():
            p1, pm, score, p2 = re.match(r'(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)', line.strip()).groups()
            sign = 1 if pm == 'gain' else -1
            happyscores[p1][p2] = sign * int(score)

    return happyscores


def calc_table_score(perm, happyscores):
    return sum(
        happyscores[perm[i - 1]][perm[i]] + happyscores[perm[i]][perm[i - 1]]
        for i in range(len(perm))
    )


def q_1(happyscores):
    people = happyscores.keys()
    optimal = max(
        calc_table_score(perm, happyscores)
        for perm in itertools.permutations(people)
    )
    return optimal


def q_2(happyscores):
    people = happyscores.keys()
    for p in people:
        happyscores['me'][p] = 0
        happyscores[p]['me'] = 0
    return q_1(happyscores)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 13 ########################################################"
    happyscores = load_happyscores()
    print "\tquestion 1 answer: {}".format(q_1(happyscores))
    print "\tquestion 2 answer: {}".format(q_2(happyscores))
