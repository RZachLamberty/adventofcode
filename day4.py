#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day4.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 4 puzzles for the advent of code (adventofcode.com/day/4)

Usage:
    <usage>

"""

import hashlib


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = 'ckczppom'


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def hash_starts_with(secret, startString):
    i = 0
    while True:
        if hashlib.md5('{}{}'.format(secret, i)).hexdigest().startswith(startString):
            return i
        i += 1


def q_1(secret):
    return hash_starts_with(secret, '00000')


def q_2(secret):
    return hash_starts_with(secret, '000000')


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 4 ########################################################"
    secret = INPUT
    print "\tquestion 1 answer: {}".format(q_1(secret))
    print "\tquestion 2 answer: {}".format(q_2(secret))
