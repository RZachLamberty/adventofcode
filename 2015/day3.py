#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day3.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 3 puzzles for the advent of code (adventofcode.com/day/3)

Usage:
    <usage>

"""

import os


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

N = '^'
E = '>'
S = 'v'
W = '<'
FNAME = os.path.join('data', 'day3_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def directions(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read()


def presents_from_dirs(dirs):
    presents = set()
    i, j = 0, 0
    presents.add((i, j))
    for d in dirs:
        if d == N:
            i += 1
        elif d == E:
            j += 1
        elif d == S:
            i -= 1
        elif d == W:
            j -= 1

        presents.add((i, j))

    return presents


def q_1(dirs):
    return len(presents_from_dirs(dirs))


def q_2(dirs):
    robodirs = [d for (i, d) in enumerate(dirs) if i % 2 == 0]
    santadirs = [d for (i, d) in enumerate(dirs) if i % 2 == 1]

    robopres = presents_from_dirs(robodirs)
    santapres = presents_from_dirs(santadirs)
    return len(robopres.union(santapres))


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 3 ########################################################"
    dirs = directions()
    print "\tquestion 1 answer: {}".format(q_1(dirs))
    print "\tquestion 2 answer: {}".format(q_2(dirs))
