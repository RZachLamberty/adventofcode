#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day13.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 13 puzzles for the advent of codec (adventofcode.com/2017/day/13)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = """0: 3
1: 2
4: 4
6: 4"""
FNAME = os.path.join('data', 'day13.txt')
LOGGER = logging.getLogger('day13')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def data_to_dict(data):
    x = {}
    for line in data.strip().split('\n'):
        d, r = line.split(": ")
        x[int(d)] = {'range': int(r), 'scanner': 0, 'scanner_dir': 1}
    return x


def q_1(data):
    firewall = data_to_dict(data)
    severity = 0
    maxdepth = max(firewall.keys())
    curdepth = -1

    for i in range(maxdepth + 1):
        curdepth += 1

        # were we caught?
        if firewall.get(i, {}).get('scanner', -1) == 0:
            LOGGER.debug('caught at depth {}!'.format(i))
            LOGGER.debug('severity before: {}'.format(severity))
            severity += i * firewall[i]['range']
            LOGGER.debug('severity after:  {}'.format(severity))

        # move all scanners
        for (depth, scannerdict) in firewall.items():
            scannerdict['scanner'] += scannerdict['scanner_dir']
            # turn around at the boundaries
            if scannerdict['scanner'] in [0, scannerdict['range'] - 1]:
                scannerdict['scanner_dir'] *= -1

    return severity


def test_q_1():
    assert q_1(TEST) == 24


def q_2(data):
    firewall = data_to_dict(data)

    # this is basically a sieve answer -- you can label "catches" as the
    # sequence of seconds at which each register returns. for example, if the
    # range is 3, every 2 * 3 - 2 seconds it will return (0, 4, 8, ...)
    # so we should be able to check modulos for our answer.
    #
    # e.g. you will be caught if (depth - delay) % (2 * range_at_depth - 2) == 0

    delay = 0
    while True:
        LOGGER.debug('checking packets delayed by {}'.format(delay))
        catches = [
            (depth + delay) % (2 * scannerdict['range'] - 2) == 0
            for depth, scannerdict in firewall.items()
        ]
        LOGGER.debug(catches)

        if not any(catches):
            return delay

        delay += 1


def test_q_2():
    assert q_2(TEST) == 10


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 13')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
