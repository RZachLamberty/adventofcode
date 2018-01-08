#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day24.py
Author: zlamberty
Created: 2017-12-24

Description:
    day 24 puzzles for the advent of codec (adventofcode.com/2017/day/24)

Usage:
    <usage>

"""

import collections
import itertools
import os
import re

import eri.logging as logging
import networkx as nx
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
FNAME = os.path.join('data', 'day24.txt')
LOGGER = logging.getLogger('day24')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return fp.read()


def gen_bridges(bridge, components):
    bridge = bridge or [(0, 0)]
    cur = bridge[-1][1]
    for b in components[cur]:
        if not ((cur, b) in bridge or (b, cur) in bridge):
            new = bridge+[(cur, b)]
            yield new
            yield from gen_bridges(new, components)


def parse_components(data):
    components = collections.defaultdict(set)
    for l in data.strip().splitlines():
        a, b = [int(x) for x in l.split('/')]
        components[a].add(b)
        components[b].add(a)
    return components


def solve(data):
    components = parse_components(data)
    mx = []
    for bridge in gen_bridges(None, components):
        mx.append((len(bridge), sum(a + b for a, b in bridge)))
    return mx


def q_1(data):
    solution = solve(data)
    return sorted(solution, key=lambda x: x[1])[-1][1]


def test_q_1():
    assert q_1(TEST) == 31


def q_2(data):
    solution = solve(data)
    return sorted(solution)[-1][1]


def test_q_2():
    assert q_2(TEST) == 19


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 24')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
