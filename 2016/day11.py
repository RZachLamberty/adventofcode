#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day11.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 11 puzzles for the advent of code (adventofcode.com/2016/day/11)

Usage:
    <usage>

"""

import itertools
import os
import re

import pprint
import tqdm

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_INSTRUCTIONS = [
    'The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.',
    'The second floor contains a hydrogen generator.',
    'The third floor contains a lithium generator.',
    'The fourth floor contains nothing relevant.',
]
FNAME = os.path.join('data', 'day11.txt')
logger = logging.getLogger('day11')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def parse_instructions(instructions):
    generators = {}
    chips = {}
    elements = set()
    for (i, instruction) in enumerate(instructions):
        for element in re.findall('([a-z]+)\-compatible', instruction):
            chips[element] = i
            elements.add(element)
        for element in re.findall('([a-z]+) generator', instruction):
            generators[element] = i
            elements.add(element)
    return generators, chips, sorted(elements)


def hash_config(elevator, generators, chips, elements):
    h = (elevator,)
    h += (tuple([generators[elem] for elem in elements]),)
    h += (tuple([chips[elem] for elem in elements]),)
    return h


def unhash_config(h, elements):
    L = len(elements)
    elevator = h[0]
    generators = dict(zip(elements, h[1]))
    chips = dict(zip(elements, h[2]))
    return elevator, generators, chips


def finished(config):
    """if every value is equal to 3 (fourth floor)"""
    e, g, c = config
    return set((e,) + g + c) == {3}


def update_hash_configs(hashConfigs, seenBefore):
    return {
        newHashConfig
        for oldHashConfig in tqdm.tqdm(hashConfigs)
        for newHashConfig in possible_hash_configs(oldHashConfig)
        if is_valid_hash_config(newHashConfig, seenBefore)
    }


def possible_hash_configs(oldHashConfig):
    e, g, c = oldHashConfig
    gc = list(g) + list(c)
    movableInds = [i for (i, elem) in enumerate(gc) if elem == e]

    for indSetLen in [1, 2]:
        for indSet in itertools.combinations(movableInds, indSetLen):
            for incr in [+1, -1]:
                eNew = e + incr
                gcNew = gc.copy()
                for i in indSet:
                    gcNew[i] += incr
                gNew, cNew = gcNew[:len(g)], gcNew[len(g):]
                yield (eNew, tuple(gNew), tuple(cNew))


def is_valid_hash_config(newHashConfig, seenBefore):
    # nothing we've already seen
    if newHashConfig in seenBefore:
        return False

    # every value should be on a floor
    e, g, c = newHashConfig
    floorVals = set((e,) + g + c)
    if floorVals.difference({0, 1, 2, 3}):
        return False

    # every chip should have either 0 generators on its level or its own
    for (i, chipfloor) in enumerate(c):
        if (chipfloor != g[i]) and any(chipfloor == gj for (j, gj) in enumerate(g) if j != i):
            return False

    return True


def q_1(data):
    elevator = 0
    generators, chips, elements = parse_instructions(data)
    hc = hash_config(elevator, generators, chips, elements)
    hashConfigs = {hc}
    seenBefore = set()

    i = 0
    while not any(finished(hc) for hc in hashConfigs):
        seenBefore.update(hashConfigs)
        hashConfigs = update_hash_configs(hashConfigs, seenBefore)
        #logger.info('possible configs:\n{}'.format(sorted(hashConfigs)))
        #input()
        logger.info('step {}'.format(i))
        logger.debug('{} possible configurations'.format(len(hashConfigs)))
        i += 1

    return i


def test_q_1():
    assert q_1(TEST_INSTRUCTIONS) == 11


def q_2(data):
    data[0] += ', an elerium generator, an elerium-compatible microchip'
    data[0] += ', a dilithium generator, and a dilithium-compatible microchip'
    return q_1(data)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 11')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
