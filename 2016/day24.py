#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day24.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 24 puzzles for the advent of code (adventofcode.com/2016/day/24)

Usage:
    <usage>

"""

import itertools
import os

import networkx as nx

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_DATA = [
    '###########',
    '#0.1.....2#',
    '#.#######.#',
    '#4.......3#',
    '###########',
]

FNAME = os.path.join('data', 'day24.txt')
logger = logging.getLogger('day24')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def q_1(data, returnTo0=False):
    I = len(data)
    J = len(data[0])
    G = nx.generators.classic.grid_2d_graph(I, J)
    specialNodes = {}
    for i in range(I):
        for j in range(J):
            if data[i][j] == '#':
                G.remove_node((i, j))
            else:
                try:
                    intnode = int(data[i][j])
                    specialNodes[intnode] = (i, j)
                except:
                    pass

    nodeDists = {}
    for (nodeVal1, nodeVal2) in itertools.combinations(specialNodes.keys(), r=2):
        d = nx.shortest_path_length(
            G,
            source=specialNodes[nodeVal1],
            target=specialNodes[nodeVal2]
        )
        nodeDists[nodeVal1, nodeVal2] = nodeDists[nodeVal2, nodeVal1] = d

    non0nodes = [k for k in specialNodes.keys() if k]
    shortestPath = None
    shortestPathLen = 1e10
    for perm in itertools.permutations(non0nodes):
        path = (0,) + perm
        if returnTo0:
            path += (0,)
        pl = sum(nodeDists[i, j] for (i, j) in zip(path[:-1], path[1:]))
        if pl < shortestPathLen:
            shortestPath = path
            shortestPathLen = pl
    logger.debug('shortest path is {}'.format(shortestPath))
    return shortestPathLen


def test_q_1():
    assert q_1(TEST_DATA) == 14


def q_2(data):
    return q_1(data, returnTo0=True)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 24')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
