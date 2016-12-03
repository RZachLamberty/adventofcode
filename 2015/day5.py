#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 5 puzzles for the advent of code (adventofcode.com/day/5)

Usage:
    <usage>

"""

import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day4_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_slist(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]


def is_nice(s, niceregs, naughtyregs):
    isnice = all(re.search(r, s) for r in niceregs)
    isnaughty = all(re.search(r, s) for r in naughtyregs) if naughtyregs else False
    return isnice and not isnaughty


def q_1(slist):
    niceregs = [
        r'[aeiou].*[aeiou].*[aeiou]',
        r'(\w)\1',
    ]
    naughtyregs = [
        r'(ab)|(cd)|(pq)|(xy)'
    ]

    return sum(is_nice(s, niceregs, naughtyregs) for s in slist)


def q_2(slist):
    niceregs = [
        r'(\w{2}).*\1',
        r'(\w{1}).{1}\1',
    ]
    naughtyregs = []

    return sum(is_nice(s, niceregs, naughtyregs) for s in slist)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 5 ########################################################"
    slist = load_slist()
    print "\tquestion 1 answer: {}".format(q_1(slist))
    print "\tquestion 2 answer: {}".format(q_2(slist))
