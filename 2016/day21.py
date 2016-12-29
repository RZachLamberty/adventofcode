#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day21.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 21 puzzles for the advent of code (adventofcode.com/2016/day/21)

Usage:
    <usage>

"""

import itertools
import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_DATA = [
    'abcde',
    [
        'swap position 4 with position 0',
        'swap letter d with letter b',
        'reverse positions 0 through 4',
        'rotate left 1 step',
        'move position 1 to position 4',
        'move position 3 to position 0',
        'rotate based on position of letter b',
        'rotate based on position of letter d',
    ]
]

FNAME = os.path.join('data', 'day21.txt')
logger = logging.getLogger('day21')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return 'abcdefgh', [line.strip() for line in f]


def rotate(s, i, direction):
    if direction == 'right':
        i = -i
    return s[i:] + s[:i]


def apply_instruction(s, instruction, reverse=False):
    m = re.match('swap position (\d+) with position (\d+)', instruction)
    if m:
        i, j = map(int, m.groups())
        s = list(s)
        s[i], s[j] = s[j], s[i]
        return ''.join(s)

    m = re.match('swap letter ([a-z]+) with letter ([a-z]+)', instruction)
    if m:
        s0, s1 = m.groups()
        return s.replace(s0, '^').replace(s1, s0).replace('^', s1)

    m = re.match('rotate (left|right) (\d+) steps?', instruction)
    if m:
        direction, i = m.groups()
        i = int(i)
        if reverse:
            direction = 'right' if direction == 'left' else 'left'
        return rotate(s, i, direction)

    m = re.match('rotate based on position of letter ([a-z]+)', instruction)
    if m:
        s0 = m.groups()[0]
        i = s.find(s0)
        if i >= 4:
            i += 1
        i += 1
        i %= len(s)
        return rotate(s, i, 'right' if not reverse else 'left')

    m = re.match('reverse positions (\d+) through (\d+)', instruction)
    if m:
        i, j = map(int, m.groups())
        return s[:i] + ''.join(reversed(s[i: j + 1])) + s[j + 1:]

    m = re.match('move position (\d+) to position (\d+)', instruction)
    if m:
        i, j = map(int, m.groups())
        s = list(s)
        si = s.pop(i)
        s.insert(j, si)
        return ''.join(s)

    raise ValueError("couldn't parse instruction {}".format(instruction))


def q_1(data, reverse=False):
    s, instructions = data
    logger.debug(s)
    for instruction in instructions:
        logger.debug(instruction)
        s = apply_instruction(s, instruction, reverse)
        logger.debug(s)
    return s


def test_q_1():
    assert q_1(TEST_DATA) == 'decab'


def q_2(data, target='fbgdceah'):
    answers = []
    s, instructions = data
    for perm in itertools.permutations(target):
        s = ''.join(perm)
        logger.info('trying string {}'.format(s))
        if q_1((s, instructions)) == target:
            answers.append(s)
    return sorted(answers)[0]


def test_q_2():
    assert q_2(TEST_DATA, 'decab') == 'abcde'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 21')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
