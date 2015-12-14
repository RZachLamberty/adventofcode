#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day2.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 2 puzzles for the advent of code (adventofcode.com/day/2)

Usage:
    <usage>

"""

import os


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day2_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def dim_list(fname=FNAME):
    with open(fname, 'r') as f:
        return [
            [int(el) for el in line.strip().split('x')]
            for line in f.readlines()
        ]


def wp(l, w, h):
    return 2 * (l * w + w * h + h * l) + (l * w * h) / max(l, w, h)


def q_1(dimlist):
    return sum(wp(*dims) for dims in dimlist)


def rl(l, w, h):
    return 2 * (l + w + h) - 2 * max(l, w, h) + l * w * h


def q_2(dimlist):
    return sum(rl(*dims) for dims in dimlist)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 2 ########################################################"
    dimlist = dim_list()
    print "\tquestion 1 answer: {}".format(q_1(dimlist))
    print "\tquestion 2 answer: {}".format(q_2(dimlist))
