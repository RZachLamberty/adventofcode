#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day23.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 23 puzzles for the advent of codec (adventofcode.com/2017/day/23)

Usage:
    <usage>

"""

import collections
import os
import re

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day23.txt')
LOGGER = logging.getLogger('day23')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_instruction(inst):
    foo, args = re.match('(set|sub|mul|jnz) (.+)', inst).groups()
    args = args.split(' ')
    return foo, args


def reg_or_int(x, reg):
    try:
        return int(x)
    except ValueError:
        return reg[x]


def apply_inst(reg, inst):
    foo, args = inst

    x = args[0]
    try:
        y = args[1]
    except IndexError:
        pass

    if foo == 'set':
        reg[x] = reg_or_int(y, reg)
    elif foo == 'sub':
        reg[x] -= reg_or_int(y, reg)
    elif foo == 'mul':
        reg[x] *= reg_or_int(y, reg)
        reg['num_muls'] += 1
    elif foo == 'jnz':
        if reg_or_int(x, reg) != 0:
            reg['jump'] = reg_or_int(y, reg)
    else:
        raise ValueError("improper instruction: {}".format(inst))


def myprint(val, N):
    LOGGER.debug(
        ''.join([
            ('x' if i == val else '.')
            for i in range(N)
        ])
    )


def q_1(data):
    insts = [parse_instruction(inst) for inst in data.splitlines()]
    reg = collections.defaultdict(int)
    i = 0
    while 0 <= i < len(insts):
        inst = insts[i]
        reg['jump'] = 1
        rcv = apply_inst(reg, inst)
        if rcv:
            break
        i += reg['jump']
        myprint(i, len(insts))
    return reg['num_muls']


def test_q_1():
    assert True


def q_2(data):
    # manually reading the instructions yields the following algorithm
    reg = collections.defaultdict(int)
    b = 109900
    c = 126900
    h = 0
    while b <= c:
        for i in range(2, b):
            if b % i == 0:
                h += 1
                break
        b += 17
    return h


def test_q_2():
    assert True


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 23')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
