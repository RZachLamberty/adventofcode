#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 7 puzzles for the advent of codec (adventofcode.com/2017/day/7)

Usage:
    <usage>

"""

import collections
import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
FNAME = os.path.join('data', 'day7.txt')
LOGGER = logging.getLogger('day7')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read()


def parse_list(s):
    """string "list" to a real data object"""
    x = {}
    for line in s.split('\n'):
        # try edge match
        match = re.match('([a-z]+) \((\d+)\) \-> ([\w,\s]+)', line)
        if match:
            (src, wt, dsts) = match.groups()
            wt = int(wt)
            dsts = dsts.split(', ')
            x[src] = {'wt': wt, 'dsts': dsts}
            continue

        match = re.match('([a-z]+) \((\d+)\)', line)
        if match:
            (src, wt) = match.groups()
            wt = int(wt)
            x[src] = {'wt': wt, 'dsts': []}
            continue

    return x


def find_root(x):
    ks = set(x.keys())
    vs = {v for vs in x.values() for v in vs['dsts']}
    d = list(ks.difference(vs))
    if len(d) != 1:
        LOGGER.debug(d)
        raise ValueError("too many unmatched keys")
    return d[0]


def q_1(s):
    x = parse_list(s)
    return find_root(x)


def test_q_1():
    assert q_1(TEST) == 'tknk'


CACHE = {}
def node_wt(x, k):
    global CACHE
    try:
        return CACHE[k]
    except:
        LOGGER.debug(k)
        v = x[k]
        nw = v['wt'] + sum(node_wt(x, _) for _ in v['dsts'])
        CACHE[k] = nw
        return CACHE[k]


def find_first_unbalanced_node(x):
    klast = None
    know = find_root(x)
    while True:
        v = x[know]
        leafs = collections.defaultdict(set)
        for subk in v['dsts']:
            leafs[node_wt(x, subk)].add(subk)
        if len(leafs) == 1:
            # it's balanced, all wts are equal. need to rebalance know to match
            # the sums in klast
            return klast, know
        for (wt, keys) in leafs.items():
            if len(keys) == 1:
                klast = know
                know = keys.pop()


def q_2(s):
    x = parse_list(s)
    kparent, kunbalanced = find_first_unbalanced_node(x)
    leafs = {_: node_wt(x, _) for _ in x[kparent]['dsts']}
    wrongwt = leafs.pop(kunbalanced)
    rightwt = list(leafs.values())[0]
    delta = rightwt - wrongwt
    return x[kunbalanced]['wt'] + delta


def test_q_2():
    assert q_2(TEST) == 60


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 7')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
