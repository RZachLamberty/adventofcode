#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day23.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 23 puzzles for the advent of code (adventofcode.com/day/23)

Usage:
    <usage>

"""

import collections
import itertools
import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day23.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_instructions():
    with open(FNAME, 'rb') as f:
        return [line.strip() for line in f]


def load_test():
    return [
        'inc a',
        'jio a, +2',
        'tpl a',
        'inc a',
    ]


def apply_instructions(register, instructions):
    instInd = 0
    while 0 <= instInd < len(instructions):
        instInd = apply_single_instruction(register, instructions, instInd)


class UndefinedInstruction(Exception):
    pass


def apply_single_instruction(reg, inst, instInd):
    i = inst[instInd]
    #print reg
    #print i
    #raw_input()
    if i.startswith('hlf'):
        regName = i.split(' ')[1]
        reg[regName] /= 2
        return instInd + 1
    elif i.startswith('tpl'):
        regName = i.split(' ')[1]
        reg[regName] *= 3
        return instInd + 1
    elif i.startswith('inc'):
        regName = i.split(' ')[1]
        reg[regName] += 1
        return instInd + 1
    elif i.startswith('jmp'):
        offset = int(i.split(' ')[1])
        return instInd + offset
    elif i.startswith('jie'):
        regName = i.split(',')[0].split(' ')[1]
        offset = int(i.split(',')[1].strip())
        return instInd + (offset if reg[regName] % 2 == 0 else 1)
    elif i.startswith('jio'):
        regName = i.split(',')[0].split(' ')[1]
        offset = int(i.split(',')[1].strip())
        return instInd + (offset if reg[regName] == 1 else 1)
    else:
        raise UndefinedInstruction()


def test():
    register = {'a': 0, 'b': 0}
    instructions = load_test()
    apply_instructions(register, instructions)
    return register


def q_1():
    register = {'a': 0, 'b': 0}
    instructions = load_instructions()
    apply_instructions(register, instructions)
    return register['b']


def q_2():
    register = {'a': 1, 'b': 0}
    instructions = load_instructions()
    apply_instructions(register, instructions)
    return register['b']


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 23 ########################################################"
    print "\tquestion 1 answer: {}".format(q_1())
    print "\tquestion 2 answer: {}".format(q_2())
