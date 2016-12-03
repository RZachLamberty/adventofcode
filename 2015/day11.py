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
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

ALPH = 'abcdefghijklmnopqrstuvwxyz'
INPUT = 'hepxcrrq'
N2A = {i: a for (i, a) in enumerate(ALPH)}
A2N = {a: i for (i, a) in enumerate(ALPH)}
L = 26


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def increment_pw(a):
    if a == '':
        return 'a'
    elif a[-1] == 'z':
        return increment_pw(a[:-1]) + 'a'
    else:
        return a[:-1] + N2A[A2N[a[-1]] + 1]


def is_valid(pw):
    return all([
        has_three_increasing(pw),
        not any(el in pw for el in ['i', 'o', 'l']),
        has_two_pairs(pw)
    ])


def has_three_increasing(pw):
    intlist = [A2N[el] for el in pw]
    inarow = 1
    lastel = intlist[0]
    for el in intlist[1:]:
        if el == lastel + 1:
            inarow += 1
            if inarow == 3:
                return True
        else:
            inarow = 1
        lastel = el
    return False


def has_two_pairs(pw):
    return re.search(r'(\w)\1.*(\w)\2', pw)


def next_pw(pw):
    newpw = increment_pw(pw)
    first4 = None
    while not is_valid(newpw):
        if newpw[:4] != first4:
            first4 = newpw[:4]
            print "new first 4: {}".format(first4)
        newpw = increment_pw(newpw)

    return newpw


def q1(pw):
    """ docstring """
    return next_pw(pw)


def q2(pw):
    """ docstring """
    return next_pw(next_pw(pw))



# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "the answer to q1: {}".format(q1(INPUT))
    print "the answer to q2: {}".format(q2(INPUT))
