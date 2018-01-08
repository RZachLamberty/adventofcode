#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day22.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 22 puzzles for the advent of codec (adventofcode.com/2017/day/22)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

U, D, L, R = 'U', 'D', 'L', 'R'
DIRS = [U, R, D, L]

INFECTED, CLEAN, WEAKENED, FLAGGED = '#', '.', 'W', 'F'

TEST = """..#
#..
...
"""
TEST_1A = (70, TEST)
TEST_1B = (10000, TEST)
TEST_2A = (100, TEST)
TEST_2B = (10000000, TEST)

FNAME = os.path.join('data', 'day22.txt')
LOGGER = logging.getLogger('day22')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return 10000, fp.read()


def nodemap_as_str(nodemap, vloc):
    imax = imin = jmax = jmin = 0
    for (i, j) in nodemap.keys():
        imax = max(i, imax)
        imin = min(i, imin)
        jmax = max(j, jmax)
        jmin = min(j, jmin)
    return '\n'.join([
        ''.join([
            'X' if ((i, j) == vloc) else nodemap[i, j]
            for j in range(jmin, jmax + 1)
        ])
        for i in range(imax, imin - 1, -1)
    ])



def make_nodemap(nodemapstr):
    lines = nodemapstr.splitlines()
    midpt = (len(lines) - 1) // 2
    nodemap = collections.defaultdict(lambda: '.')
    for (i, row) in enumerate(lines, start=-midpt):
        for (j, char) in enumerate(row, start=-midpt):
            nodemap[-i, j] = char
    return nodemap


def left(d):
    return DIRS[(DIRS.index(d) - 1) % len(DIRS)]


def right(d):
    return DIRS[(DIRS.index(d) + 1) % len(DIRS)]


def rev(d):
    return DIRS[(DIRS.index(d) + 2) % len(DIRS)]


def update(nodemapstr, vloc, vdir, updatedict):
    currstate = nodemapstr[vloc]
    # direction
    if currstate == INFECTED:
        vdir = right(vdir)
    elif currstate == CLEAN:
        vdir = left(vdir)
    elif currstate == WEAKENED:
        # do nothing, but don't raise an error
        pass
    elif currstate == FLAGGED:
        vdir = rev(vdir)
    else:
        LOGGER.debug('nodemapstr: {}'.format(nodemapstr))
        LOGGER.debug('vloc: {}'.format(vloc))
        LOGGER.debug('vdir: {}'.format(vdir))
        LOGGER.debug('updatedict: {}'.format(updatedict))
        raise ValueError("wtf is this state: {}".format(currstate))

    # update the current square and mark if this was an infection
    nodemapstr[vloc] = updatedict[currstate]
    infect = nodemapstr[vloc] == INFECTED

    # move
    i, j = vloc
    if vdir == U:
        vloc = i + 1, j
    elif vdir == D:
        vloc = i - 1, j
    elif vdir == L:
        vloc = i, j - 1
    elif vdir == R:
        vloc = i, j + 1
    else:
        raise ValueError("wtf is this direction: {}".format(vdir))

    return vloc, vdir, infect


def q_1(data):
    numiters, nodemapstr = data
    nodemap = make_nodemap(nodemapstr)
    updatedict = {INFECTED: CLEAN, CLEAN: INFECTED}
    vloc = (0, 0)
    vdir = U
    infections = 0
    for i in tqdm.trange(numiters):
        vloc, vdir, caused_infection = update(nodemap, vloc, vdir, updatedict)
        infections += caused_infection
        #LOGGER.debug(
        #    'after {} steps\n{}'.format(i, nodemap_as_str(nodemap, vloc))
        #)
    return infections


def test_q_1():
    assert q_1(TEST_1A) == 41
    assert q_1(TEST_1B) == 5587


def q_2(data):
    numiters, nodemapstr = data
    numiters = 10000000
    nodemap = make_nodemap(nodemapstr)
    updatedict = {
        CLEAN: WEAKENED,
        WEAKENED: INFECTED,
        INFECTED: FLAGGED,
        FLAGGED: CLEAN,
    }
    vloc = (0, 0)
    vdir = U
    infections = 0
    for i in tqdm.trange(numiters):
        vloc, vdir, caused_infection = update(nodemap, vloc, vdir, updatedict)
        infections += caused_infection
        #LOGGER.debug(
        #    'after {} steps\n{}'.format(i, nodemap_as_str(nodemap, vloc))
        #)
    return infections


def test_q_2():
    assert q_2(TEST_2A) == 26
    assert q_2(TEST_2B) == 2511944


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 22')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
