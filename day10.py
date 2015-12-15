#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day10.py
Author: zlamberty
Created: 2015-12-09

Description:


Usage:
    <usage>

"""

import os


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = '1113122113'


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def look_and_say(x):
    o = ''
    currnum = 1
    lastn = x[0]
    for thisn in x[1:]:
        if thisn == lastn:
            currnum += 1
        else:
            o += '{}{}'.format(currnum, lastn)
            currnum = 1
            lastn = thisn
    o += '{}{}'.format(currnum, lastn)
    return o


def q1(x):
    """ docstring """
    i = 0
    while i < 40:
        x = look_and_say(x)
        i += 1

    return len(x)


def q2(x):
    """ docstring """
    i = 0
    while i < 50:
        x = look_and_say(x)
        i += 1

    return len(x)



# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "the answer to q1: {}".format(q1(INPUT))
    print "the answer to q2: {}".format(q2(INPUT))
