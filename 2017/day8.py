#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 8 puzzles for the advent of codec (adventofcode.com/2017/day/8)

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

TEST = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
FNAME = os.path.join('data', 'day8.txt')
LOGGER = logging.getLogger('day8')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def parse_instruction(inst):
    reg, incdec, val, compreg, comp, compval = re.match(
        '(\w+) (inc|dec) ([\-\d]+) if (\w+) ([!=<>]{1,2}) ([\-\d]+)', inst
    ).groups()
    val = int(val)
    compval = int(compval)
    return reg, incdec, val, compreg, comp, compval


def parse_instructions(s):
    return [
        parse_instruction(line)
        for line in s.strip().split('\n')
    ]


def check_comp(register, compreg, comp, compval):
    regval = register[compreg]
    if comp == '>':
        return regval > compval
    elif comp == '>=':
        return regval >= compval
    elif comp == '<':
        return regval < compval
    elif comp == '<=':
        return regval <= compval
    elif comp == '==':
        return regval == compval
    elif comp == '!=':
        return regval != compval
    else:
        raise ValueError('false comparison')


def q_1(s):
    insts = parse_instructions(s)
    register = collections.defaultdict(int)

    for (reg, incdec, val, compreg, comp, compval) in insts:
        if check_comp(register, compreg, comp, compval):
            register[reg] += (1 if incdec == 'inc' else -1) * val

    maxk, maxv = max(register.items(), key=lambda kv: kv[1])

    return maxv


def test_q_1():
    assert q_1(TEST) == 1


def q_2(s):
    insts = parse_instructions(s)
    register = collections.defaultdict(int)

    maxv = 0

    for (reg, incdec, val, compreg, comp, compval) in insts:
        if check_comp(register, compreg, comp, compval):
            register[reg] += (1 if incdec == 'inc' else -1) * val
            maxk, maxvnow = max(register.items(), key=lambda kv: kv[1])
            maxv = max(maxvnow, maxv)

    return maxv


def test_q_2():
    assert q_2(TEST) == 10


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 8')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
