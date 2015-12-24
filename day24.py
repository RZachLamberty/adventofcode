#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day24.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 24 puzzles for the advent of code (adventofcode.com/day/24)

Usage:
    <usage>

"""

import collections
import itertools
import os
import re
import pickle
import scipy


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day24.txt')
CACHE = os.path.join(os.sep, 'tmp', 'triads.{num:}.pkl')
TESTCACHE = os.path.join(os.sep, 'tmp', 'testtriads.{num:}.pkl')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_intlist():
    with open(FNAME, 'rb') as f:
        return [int(line.strip()) for line in f]


def load_test():
    return [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]


def get_groups(intlist, num=3, cachefile=CACHE):
    cachefile = cachefile.format(num=num)
    try:
        with open(cachefile, 'rb') as f:
            return pickle.load(f)
    except:
        tot = sum(intlist)
        grptot = tot / num
        grps = []
        for i in range(len(intlist) - 2):
            grpsThisRound = False
            for comb in itertools.combinations(intlist, i):
                if sum(comb) == grptot:
                    grpsThisRound = True
                    grps.append(set(comb))
            if grps and not grpsThisRound:
                break
        with open(cachefile, 'wb') as f:
            pickle.dump(grps, f)
        return grps


def santamin(grp):
    return (len(grp), scipy.product(list(grp)))


def test():
    intlist = load_test()
    triads = get_groups(intlist, cachefile=TESTCACHE)

    x = itergroups(triads).next()
    print 'group 1: {}'.format(x)
    print 'QE     : {}'.format(scipy.product(list(x[0])))

    quads = get_groups(intlist, num=4, cachefile=TESTCACHE)
    x = itergroups(quads, num=4).next()
    print 'group 1: {}'.format(x)
    print 'QE     : {}'.format(scipy.product(list(x[0])))


def itergroups(groups, num=3):
    """ compile a list of all sets of num groups which are mututally
        exclusive

    """
    sortedgroups = sorted(groups, key=santamin)

    for c in sortedgroups:
        if num == 1:
            yield (c,)
        else:
            others = (
                t for t in sortedgroups
                if not set.intersection(t, c)
            )
            for subgrp in itergroups(others, num=num - 1):
                yield (c,) + subgrp


def itertriads(triads):
    # sort that shit
    sortedtriads = sorted(triads, key=santamin)
    for c1 in sortedtriads:
        print c1
        others = (
            t for t in triads
            and not set.intersection(t, c1)
        )
        for c2 in others:
            stillothers = (
                t for t in others
                if not set.intersection(t, c1, c2)
            )
            for c3 in stillothers:
                yield (c1, c2, c3)


def iterquads(quads):
    # sort that shit
    sortedquads = sorted(quads, key=santamin)
    for c1 in sortedquads:
        print c1
        others = (
            t for t in quads
            and not set.intersection(t, c1)
        )
        for c2 in others:
            stillothers = (
                t for t in others
                if not set.intersection(t, c1, c2)
            )
            for c3 in stillothers:
                evenothers = (
                    t for t in stillothers
                    if not set.intersection(t, c1, c2, c3)
                )
                for c4 in evenothers:
                    yield (c1, c2, c3, c4)


def f(num=3):
    intlist = load_intlist()
    groups = get_groups(intlist, num=num)

    return scipy.product(list(itergroups(groups).next()[0]))


def q_1():
    return f(3)


def q_2():
    return f(4)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 24 ########################################################"
    print "\tquestion 1 answer: {}".format(q_1())
    print "\tquestion 2 answer: {}".format(q_2())
