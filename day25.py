#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day25.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 25 puzzles for the advent of code (adventofcode.com/day/25)

Usage:
    <usage>

"""

import collections
import itertools
import os
import re
import scipy


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

START = 20151125
A = 252533
B = 33554393
FNAME = os.path.join('data', 'day25.txt')


import collections
import functools

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if len(self.cache) > 100:
            self.cache.pop(min(self.cache.keys()))
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_input():
    return 3010, 3019


def load_test():
    return scipy.array([
        [20151125, 18749137, 17289845, 30943339, 10071777, 33511524],
        [31916031, 21629792, 16929656, 7726640, 15514188, 4041754],
        [16080970, 8057251, 1601130, 7981243, 11661866, 16474243],
        [24592653, 32451966, 21345942, 9380097, 10600672, 31527494],
        [77061, 17552253, 28094349, 6899651, 9250759, 31663883],
        [33071741, 6796745, 25397450, 24659492, 1534922, 27995004],
    ])


@memoized
def int_to_coord(i):
    if i == 0:
        return (0, 0)
    a, b = int_to_coord(i - 1)
    if a > 0:
        return a - 1, b + 1
    else:
        return b + 1, 0


def coord_to_i(r, c):
    s = r + c
    return s * (s + 1) / 2 + c + 1


def next_val(x):
    if x is None:
        return START
    return (x * A) % B


def test():
    t = load_test()
    z = scipy.zeros((20, 20))
    z[0, 0] = START
    for el in range(1, 11 * 11):
        inow, jnow = int_to_coord(el)
        iprev, jprev = int_to_coord(el - 1)
        z[inow, jnow] = next_val(z[iprev, jprev])

    assert (t == z[:6, :6]).all()


def q_1(input):
    r, c = input
    r -= 1
    c -= 1
    i = 0
    v = None
    while True:
        rnow, cnow = int_to_coord(i)
        if rnow == r:
            print (rnow, cnow)
        v = next_val(v)
        if (rnow, cnow) == (r, c):
            return v
        i += 1


def q_1_fast(input):
    r, c = input
    r -= 1
    c -= 1
    v = None
    for i in xrange(coord_to_i(r, c)):
        v = next_val(v)
    return v


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 25 ########################################################"
    input = load_input()
    print "\tquestion 1 answer: {}".format(q_1(input))
    print "\tquestion 2 answer: {}".format(q_2(input))
