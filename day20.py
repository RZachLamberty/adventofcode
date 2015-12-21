#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day20.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 20 puzzles for the advent of code (adventofcode.com/day/20)

Usage:
    <usage>

"""


from collections import defaultdict

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

#FNAME = os.path.join('data', 'day20.txt')
INPUT = 36000000

# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def sum_of_factors(x):
    return sum([n for n in xrange(1,x) if x % n == 0])


def q_1(input, maxhouse=INPUT / 10):
    visits = defaultdict(int)
    for i in range(1, maxhouse):
        for house in (i * step for step in range(1, maxhouse/i)):
            visits[house] += i * 10
    return min(k for k in visits if visits[k] >= input)


def q_2(input, maxhouse=INPUT / 10):
    visits = defaultdict(int)
    for i in range(1, maxhouse):
        for house in (i * step for step in range(1, min(50, maxhouse/i))):
            visits[house] += i * 11
    return min(k for k in visits if visits[k] >= input)



# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 20 ########################################################"
    input = INPUT
    print "\tquestion 1 answer: {}".format(q_1(input))
    print "\tquestion 2 answer: {}".format(q_2(input))
