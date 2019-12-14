#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day19.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 19 puzzles for the advent of code (adventofcode.com/2016/day/19)

Usage:
    <usage>

"""

import collections
import math

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

INPUT = 3018458
logger = logging.getLogger('day19')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data():
    return INPUT


def update_presents(presents, numelves):
    i0 = 1
    while i0 <= numelves:
        if i0 not in presents:
            i0 += 1
        else:

            i1 = i0 + 1
            while i1 not in presents:
                i1 += 1
                i1 %= numelves
            presents[i0] += presents.pop(i1)

def q_1(data):
    presents = {i: 1 for i in range(data)}

    numelves = data
    i0 = 0
    while len(presents) > 1:
        # chem_get next active elf
        if i0 in presents:
            # chem_get next present-baring elf
            i1 = (i0 + 1) % numelves
            while i1 not in presents:
                i1 += 1
                i1 %= numelves
            numpres = presents.pop(i1)
            logger.info('elf {} steals {} presents from elf {}'.format(i0 + 1, numpres, i1 + 1))
            presents[i0] += numpres

        i0 += 1
        i0 %= numelves

    return list(presents.keys())[0] + 1


def test_q_1():
    assert q_1(5) == 3


def q_2(data):
    numelves = data
    presents = list(range(numelves))
    i0 = 0
    i1 = math.floor(numelves / 2)
    while numelves > 1:
        elf0 = presents[i0]
        elf1 = presents[i1]

        debug = (numelves % 1000 == 0)
        #debug = True
        if debug:
            logger.debug('i0 = {}'.format(i0))
            logger.debug('elf0 = {}'.format(elf0))
            logger.debug('i1 = {}'.format(i1))
            logger.debug('elf1 = {}'.format(elf1))
            logger.debug('numelves = {}'.format(numelves))

        presents.pop(i1)

        numelves = len(presents)

        if 2 * i0 < numelves:
            i0 += 1

        if numelves % 2 == 0:
            i1 += 1

        i0 %= numelves
        i1 %= numelves

    return presents[0] + 1


def test_q_2():
    assert q_2(5) == 2


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 19')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
