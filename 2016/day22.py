#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day22.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 22 puzzles for the advent of code (adventofcode.com/2016/day/22)

Usage:
    <usage>

"""

import itertools
import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_DATA = [
    [0, 0, 10, 8, 2, 80],
    [0, 1, 11, 6, 5, 54],
    [0, 2, 32, 28, 4, 87],
    [1, 0, 9, 7, 2, 77],
    [1, 1, 8, 0, 8, 0],
    [1, 2, 11, 7, 4, 63],
    [2, 0, 10, 6, 4, 60],
    [2, 1, 9, 8, 1, 88],
    [2, 2, 9, 6, 3, 66],
]

FNAME = os.path.join('data', 'day22.txt')
logger = logging.getLogger('day22')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        f.readline()
        f.readline()
        return [
            list(
                map(
                    int,
                    re.match(
                        '.*\-x(\d+)\-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%',
                        line.strip()
                    ).groups()
                )
            )
            for line in f
        ]


def is_viable(n0, n1):
    return n0['used'] and n0['used'] <= n1['avail']


def q_1(data):
    nodes = [
        dict(zip(['ix', 'iy', 'size', 'used', 'avail', 'usedPerc'], row))
        for row in data
    ]

    return sum(is_viable(n0, n1) for (n0, n1) in itertools.permutations(nodes, 2))


def print_nodes_usvals(nodes):
    x = {(n['ix'], n['iy']): n for n in nodes}

    ixmax = max(k[0] for k in x.keys())
    iymax = max(k[1] for k in x.keys())

    for iy in range(iymax + 1):
        for ix in range(ixmax + 1):
            print('{used:}/{size:}'.format(**x[ix, iy]).center(9), end='')
        print()


def print_nodes_symbolic(nodes):
    x = {(n['ix'], n['iy']): n for n in nodes}

    ixmax = max(k[0] for k in x.keys())
    iymax = max(k[1] for k in x.keys())

    curHoleSize = 0
    for node in nodes:
        if node['used'] == 0:
            if node['avail'] >= curHoleSize:
                curHoleSize = node['avail']
                ixHole = node['ix']
                iyHole = node['iy']

    for iy in range(iymax + 1):
        for ix in range(ixmax + 1):
            szchar = '#' if x[ix, iy]['used'] > curHoleSize else '.'

            if ix == ixHole and iy == iyHole:
                char = ' _ '
            elif iy == 0 and ix == ixmax:
                char = ' G '
            elif iy == 0 and ix == 0:
                char = '({})'.format(szchar)
            else:
                char = ' {} '.format(szchar)

            print(char, end='')
        print()


def q_2(data):
    nodes = [
        dict(zip(['ix', 'iy', 'size', 'used', 'avail', 'usedPerc'], row))
        for row in data
    ]

    print_nodes_symbolic(nodes)
    logger.warning(
        "i just counted it by hand, direct sprint to G and 5-step movement of "
        "G along the edge to the origin"
    )


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 22')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
