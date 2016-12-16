#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day12.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 12 puzzles for the advent of code (adventofcode.com/2016/day/12)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day12.txt')
logger = logging.getLogger('day12')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def parse_instructions(data):
    instructions = []
    for inst in data:
        l = inst.split(' ')
        for (i, li) in enumerate(l):
            try:
                l[i] = int(li)
            except ValueError:
                continue
        instructions.append(l)
    return instructions


def apply_instruction(registers, instruction):
    #logger.debug(instruction)
    com = instruction[0]
    increment = 1

    if com == 'cpy':
        x, y = instruction[1:]
        registers[y] = registers.get(x, x)
    elif com == 'inc':
        x = instruction[1]
        registers[x] += 1
    elif com == 'dec':
        x = instruction[1]
        registers[x] -= 1
    elif com == 'jnz':
        x, y = instruction[1:]
        if registers.get(x, x) != 0:
            increment = y

    #logger.debug(registers)
    return increment


def q_1(data, register='a', pt2=False):
    registers = {char: 0 for char in 'abcd'}

    if pt2:
        registers['c'] = 1

    instructions = parse_instructions(data)

    i = 0
    L = len(instructions)
    while i < L:
        instruction = instructions[i]
        increment = apply_instruction(registers, instruction)
        i += increment
        #print('#' * i + '-' * (L - i))

    return registers[register]


def test_q_1():
    assert q_1([
        'cpy 41 a',
        'inc a',
        'inc a',
        'dec a',
        'jnz a 2',
        'dec a',
    ], register='a') == 42


def q_2(data, register='a'):
    return q_1(data, register, pt2=True)


def test_q_2():
    assert q_2(None) == None


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 12')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
