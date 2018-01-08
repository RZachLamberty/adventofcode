#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day25.py
Author: zlamberty
Created: 2017-12-25

Description:
    day 25 puzzles for the advent of codec (adventofcode.com/2017/day/25)

Usage:
    <usage>

"""

import collections
import os

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

L, R = -1, 1
Inst = collections.namedtuple(
    'Instruction',
    ['writeval', 'cursordelta', 'nextstate']
)
TEST_INST = {
    'a': {
        0: Inst(1, R, 'b'),
        1: Inst(0, L, 'b'),
    },
    'b': {
        0: Inst(1, L, 'a'),
        1: Inst(1, R, 'a'),
    },
}
TEST = ('a', 6, TEST_INST)
FNAME = os.path.join('data', 'day25.txt')
LOGGER = logging.getLogger('day25')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    return (
        'a',
        12861455,
        {
            'a': {
                0: Inst(1, R, 'b'),
                1: Inst(0, L, 'b'),
            },
            'b': {
                0: Inst(1, L, 'c'),
                1: Inst(0, R, 'e'),
            },
            'c': {
                0: Inst(1, R, 'e'),
                1: Inst(0, L, 'd'),
            },
            'd': {
                0: Inst(1, L, 'a'),
                1: Inst(1, L, 'a'),
            },
            'e': {
                0: Inst(0, R, 'a'),
                1: Inst(0, R, 'f'),
            },
            'f': {
                0: Inst(1, R, 'e'),
                1: Inst(1, R, 'a'),
            },
        }
    )


def apply_instructions(tape, cursor, state, blueprint):
    inst = blueprint[state][tape[cursor]]
    tape[cursor] = inst.writeval
    cursor += inst.cursordelta
    state = inst.nextstate
    return cursor, state


def q_1(data):
    tape = collections.defaultdict(int)
    cursor = 0
    state, numsteps, blueprint = data
    LOGGER.debug(tape)
    for i in tqdm.trange(numsteps):
        cursor, state = apply_instructions(tape, cursor, state, blueprint)
        LOGGER.debug(tape)
    return sum(tape.values())


def test_q_1():
    assert q_1(TEST) == 3


def q_2(data):
    return


def test_q_2():
    assert True


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 25')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
