#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day9.py
Author: zlamberty
Created: 2015-12-09

Description:
    day 9 puzzles for the advent of code (adventofcode.com/day/9)

Usage:
    <usage>

"""

import itertools
import os
import re

from collections import defaultdict


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day9_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_distances(fname=FNAME):
    distances = defaultdict(dict)
    with open(fname, 'r') as f:
        for line in f.readlines():
            a, b, d = re.match(r'(\w+) to (\w+) = (\d+)', line.strip()).groups()
            d = int(d)
            distances[a][b] = d
            distances[b][a] = d

    return distances


def path_dist(path, distances):
    return sum(
        distances[path[i]][path[i + 1]]
        for i in range(len(path) - 1)
    )


def q_1(distances):
    sites = distances.keys()
    minpath = min(
        itertools.permutations(sites),
        key=lambda path: path_dist(path, distances)
    )

    return path_dist(minpath, distances)


def q_2(distances):
    sites = distances.keys()
    minpath = max(
        itertools.permutations(sites),
        key=lambda path: path_dist(path, distances)
    )

    return path_dist(minpath, distances)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 9 ########################################################"
    distances = load_distances()
    print "\tquestion 1 answer: {}".format(q_1(distances))
    print "\tquestion 2 answer: {}".format(q_2(distances))
