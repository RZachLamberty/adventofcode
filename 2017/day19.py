#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day19.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 19 puzzles for the advent of codec (adventofcode.com/2017/day/19)

Usage:
    <usage>

"""

import os

import eri.logging as logging
import networkx as nx
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = (
    '     |          \n'
    '     |  +--+    \n'
    '     A  |  C    \n'
    ' F---|--|-E---+ \n'
    '     |  |  |  D \n'
    '     +B-+  +--+ \n'
    '                  '
)
U, D, R, L = 'U', 'D', 'R', 'L'
BACKWARDS = {U: D, D: U, R: L, L: R,}
FNAME = os.path.join('data', 'day19.txt')
LOGGER = logging.getLogger('day19')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return fp.read()


def walk(ar, i0, j0, direction):
    if direction in [U, D]:
        if direction == D:
            step = 1
            lim = len(ar)
        else:
            step = -1
            lim = -1
        for i in range(i0 + step, lim, step):
            yield i, j0
    else:
        if direction == R:
            step = 1
            lim = len(ar[0])
        elif direction == L:
            step = -1
            lim = -1
        for j in range(j0 + step, lim, step):
            yield i0, j


def find_out_direction(ar, n1, indirection):
    i1, j1 = n1
    directions = [U, D, R, L]
    directions.remove(BACKWARDS[indirection])
    for outdirection in directions:
        if outdirection == U and i1 > 0 and ar[i1 - 1][j1] != ' ':
            return U
        elif outdirection == D and i1 < len(ar) - 1 and ar[i1 + 1][j1] != ' ':
            return D
        elif outdirection == L and j1 > 0 and ar[i1][j1 - 1] != ' ':
            return L
        elif outdirection == R and i1 < len(ar[0]) - 1 and ar[i1][j1 + 1] != ' ':
            return R
    return None


def find_next_node(ar, n0, direction):
    i0, j0 = n0
    steps = 0

    # find the next node location; capture letters and steps along the way
    for (i1, j1) in walk(ar, i0, j0, direction):
        steps += 1
        c1 = ar[i1][j1]
        if c1 == '+' or c1.isalpha():
            # we've found a turning node or a letter node, break
            break
        elif c1 == ' ':
            raise ValueError('walked beyond the crossing...')

    n1 = i1, j1
    c1 = ar[i1][j1]
    isletter = c1.isalpha()

    # figure out the next direction out. if there is none and this is a letter,
    # we're done
    outdirection = find_out_direction(ar, n1, indirection=direction)
    isend = (outdirection is None) and isletter
    return n1, outdirection, isend, steps, isletter, c1


def im_to_g(im):
    """convert the ascii image to a networkx graph"""
    g = nx.DiGraph()

    # first, to array
    ar = [list(row) for row in im.splitlines()]

    # find the starting point and make node 0 -- it should be a single pipe
    # character in the first row
    rootnode = n0 = (0, ar[0].index('|'))
    outdir = D
    isend = False

    while not isend:
        LOGGER.debug('n0: {}'.format(n0))
        LOGGER.debug('c0: {}'.format(ar[n0[0]][n0[1]]))
        LOGGER.debug('d:  {}'.format(outdir))
        n1, outdir, isend, steps, isletter, c1 = find_next_node(ar, n0, outdir)
        g.add_edge(n0, n1, steps=steps)
        g.node[n1].update({
            'isletter': isletter,
            'nodeval': c1,
        })
        n0 = n1

    return g


def q_1(data):
    g = im_to_g(data)
    return ''.join([
        d['nodeval']
        for (n, d) in g.nodes(data=True)
        if d.get('isletter')
    ])


def test_q_1():
    assert q_1(TEST) == 'ABCDEF'


def q_2(data):
    g = im_to_g(data)
    return sum(e['steps'] for (n0, n1, e) in g.edges(data=True)) + 1


def test_q_2():
    assert q_2(TEST) == 38


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 19')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
