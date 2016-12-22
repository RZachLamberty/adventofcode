#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day17.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 17 puzzles for the advent of code (adventofcode.com/2016/day/17)

Usage:
    <usage>

"""

import collections
import functools
import hashlib

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = 'yjjvjgan'
logger = logging.getLogger('day17')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


@functools.lru_cache(maxsize=None)
def path_to_loc(path):
    c = collections.Counter(path)
    return [c['D'] - c['U'], c['R'] - c['L']]


def open_door_directions(path, passcode):
    i, j = path_to_loc(path)

    x = hashlib.md5('{}{}'.format(passcode, path).encode()).hexdigest()[:4]

    for (direction, char) in zip('UDLR', x):
        if any([i == 0 and direction == 'U',
                i == 3 and direction == 'D',
                j == 0 and direction == 'L',
                j == 3 and direction == 'R']):
            continue
        if char >= 'b':
            yield direction


def take_steps(paths, passcode):
    newpaths = set()
    for path in paths:
        for direction in open_door_directions(path, passcode):
            newpaths.add(path + direction)
    return newpaths


def made_it(path):
    return path_to_loc(path) == [3, 3]


def q_1(data):
    pathsSoFar = {''}

    while pathsSoFar:
        pathsSoFar = take_steps(paths=pathsSoFar, passcode=data)
        for path in pathsSoFar:
            if made_it(path):
                return path

    raise ValueError('no more valid paths!')


def test_q_1():
    assert q_1('ihgpwlah') == 'DDRRRD'
    assert q_1('kglvqrro') == 'DDUDRLRRUDRD'
    assert q_1('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'


def q_2(data):
    pathsSoFar = {''}

    longestWinner = 0

    while pathsSoFar:
        pathsSoFar = take_steps(paths=pathsSoFar, passcode=data)
        winningPaths = {path for path in pathsSoFar if made_it(path)}
        pathsSoFar = pathsSoFar.difference(winningPaths)

        for wp in winningPaths:
            longestWinner = max(longestWinner, len(wp))

    return longestWinner


def test_q_2():
    assert q_2('ihgpwlah') == 370
    assert q_2('kglvqrro') == 492
    assert q_2('ulqzkmiv') == 830


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 17')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
