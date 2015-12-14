#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day1.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 1 puzzles for the advent of code (adventofcode.com/day/1)

Usage:
    <usage>

"""

import os


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

UP = '('
DOWN = ')'
BASEMENT = -1
FNAME = os.path.join('data', 'day1_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_dirs(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read()


def q_1(directions):
    up = max(directions.count(UP), 0)
    down = max(directions.count(DOWN), 0)
    return up - down


def q_2(directions):
    flr = 0
    for (i, el) in enumerate(directions):
        if el == UP:
            flr += 1
        elif el == DOWN:
            flr -= 1

        if flr == BASEMENT:
            return i + 1

    return "Never made it to the basement"


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 1 ########################################################"
    dirs = load_dirs()
    print "\tquestion 1 answer: {}".format(q_1(dirs))
    print "\tquestion 2 answer: {}".format(q_2(dirs))
