#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day12.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 12 puzzles for the advent of codec (adventofcode.com/2017/day/12)

Usage:
    <usage>

"""

import collections
import os
import re

import eri.logging as logging
import networkx as nx


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
FNAME = os.path.join('data', 'day12.txt')
LOGGER = logging.getLogger('day12')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read()


def data_to_dict(data):
    x = collections.defaultdict(set)
    for line in data.strip().split('\n'):
        src, dsts = re.match('(\d+) <\-> ([\d,\s]+)', line).groups()
        src = int(src)
        dsts = [int(_) for _ in dsts.split(', ')]
        x[src].update(dsts)
    return x


def q_1(data):
    x = data_to_dict(data)

    reachable = {0,}
    while True:
        also = set()
        for prog0 in reachable:
            for prog1 in x[prog0]:
                also.add(prog1)
        # did we see a new program?
        if also.difference(reachable):
            reachable.update(also)
        else:
            break
    return len(reachable)


def q_1_nx(data):
    # solve with networkx
    g = nx.Graph(data_to_dict(data))
    return len(nx.node_connected_component(g, 0))


def test_q_1():
    assert q_1(TEST) == 6
    assert q_1_nx(TEST) == 6



def q_2(data):
    x = data_to_dict(data)

    unseen = set(x.keys())
    components = []
    while unseen:
        LOGGER.debug('unseen = {}'.format(unseen))
        comp = {unseen.pop(),}
        while True:
            also = set()
            for prog0 in comp:
                for prog1 in x[prog0]:
                    also.add(prog1)
            # did we see a new program?
            if also.difference(comp):
                comp.update(also)
            else:
                break
        LOGGER.debug('comp = {}'.format(comp))
        unseen = unseen.difference(comp)
        components.append(comp)
    return len(components)


def q_2_nx(data):
    g = nx.Graph(data_to_dict(data))
    return nx.number_connected_components(g)


def test_q_2():
    assert q_2(TEST) == 2
    assert q_2_nx(TEST) == 2


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 12')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
