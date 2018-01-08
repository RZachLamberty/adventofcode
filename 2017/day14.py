#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day14.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 14 puzzles for the advent of codec (adventofcode.com/2017/day/14)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging
import networkx as nx

import utils


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day14.txt')
LOGGER = logging.getLogger('day14')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    return 'nbysizxe'


def build_array(data):
    return [
        utils.knot_hash_to_bin(utils.knot_hash((256, '{}-{}'.format(data, i))))
        for i in range(128)
    ]


def q_1(data):
    array = build_array(data)
    c = collections.Counter()
    for row in array:
        c.update(row)
    return c['1']


def test_q_1():
    assert q_1('flqrgnkx') == 8108


def q_2(data):
    array = build_array(data)
    g = nx.grid_2d_graph(128, 128)
    for (i, row) in enumerate(array):
        for (j, char) in enumerate(row):
            if char == '0':
                g.remove_node((i, j))

    return nx.number_connected_components(g)


def test_q_2():
    assert q_2('flqrgnkx') == 1242


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 14')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
