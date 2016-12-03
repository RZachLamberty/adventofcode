#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day17.py
Author: zlamberty
Created: 2015-12-09

Description:
    day 17 puzzles for the advent of code (adventofcode.com/day/17)

Usage:
    <usage>

"""

import itertools
import os

from collections import defaultdict


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day17.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_containers(fname=FNAME):
    with open(fname, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def vol(containers, combo):
    return sum(
        size * num
        for (size, num) in zip(containers, combo)
    )


def q_1(containers, target=150):
    return sum(
        vol(containers, combo) == target
        for combo in itertools.product(*[range(2) for el in containers])
    )


def q_2(containers, target=150):
    x = defaultdict(set)
    for combo in itertools.product(*[range(2) for el in containers]):
        if vol(containers, combo) == target:
            x[sum(combo)].add(combo)

    minvol = min(x.keys())
    return len(x[minvol])


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 17 ########################################################"
    containers = load_containers()
    print "\tquestion 1 answer: {}".format(q_1(containers))
    print "\tquestion 2 answer: {}".format(q_2(containers))
