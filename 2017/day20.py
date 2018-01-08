#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day20.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 20 puzzles for the advent of codec (adventofcode.com/2017/day/20)

Usage:
    <usage>

"""

import collections
import functools
import os
import re

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
TEST_2 = """p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>"""
FNAME = os.path.join('data', 'day20.txt')
LOGGER = logging.getLogger('day20')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return fp.read()


def parse_data(data):
    return [
        [int(_) for _ in re.findall('[-\d]+', line)]
        for line in data.splitlines()
    ]


def _acoef(n):
    if n == 0:
        return 0
    return sum(range(n))


@functools.lru_cache(maxsize=None)
def _acoef_recur(n):
    if n == 0:
        return 0
    return n + _acoef_recur(n - 1)


def integrate(pva, n):
    px, py, pz, vx, vy, vz, ax, ay, az = pva
    return [
        px + n * vx + _acoef(n) * ax,
        py + n * vy + _acoef(n) * ay,
        pz + n * vz + _acoef(n) * az,
    ]


def integrate_recur(pva, n):
    px, py, pz, vx, vy, vz, ax, ay, az = pva
    return [
        px + n * vx + _acoef_recur(n) * ax,
        py + n * vy + _acoef_recur(n) * ay,
        pz + n * vz + _acoef_recur(n) * az,
    ]


def metropolis(x):
    return sum(abs(_) for _ in x)


def q_1(data):
    pvas = parse_data(data)
    imin, pvamin = min(
        enumerate(pvas),
        key=lambda elem: metropolis(integrate(elem[1], 1000))
    )
    return imin


def test_q_1():
    assert q_1(TEST) == 0


def q_2(data):
    pvas = parse_data(data)
    collisions = [False for i in range(len(pvas))]

    for i in range(1, 1000):
        LOGGER.debug("at step {}".format(i))
        seen = collections.defaultdict(set)
        for (j, (pva, collision)) in enumerate(zip(pvas, collisions)):
            if not collision:
                seen[tuple(integrate_recur(pva, i))].add(j)

        # mark collisions as dead
        for (dist, indset) in seen.items():
            if len(indset) > 1:
                for j in indset:
                    LOGGER.debug("removing item {}".format(j))
                    collisions[j] = True

    return len(collisions) - sum(collisions)


def test_q_2():
    assert q_2(TEST_2) == 1


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 20')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
