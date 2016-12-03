#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day6.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 6 puzzles for the advent of code (adventofcode.com/day/6)

Usage:
    <usage>

"""

import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day6_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_instructions(fname=FNAME):
    with open(fname, 'r') as f:
        return [parse_inst(line.strip()) for line in f.readlines()]


def parse_inst(inst):
    r = re.search(
        '(turn on|turn off|toggle) (\d{,3}),(\d{,3}) through (\d{,3}),(\d{,3})',
        inst
    ).groups()
    cmd = r[0]
    i0, j0, i1, j1 = [int(el) for el in r[1:]]
    return cmd, i0, j0, i1, j1


def update_lights(lights, inst, cmdmap):
    cmd, i0, j0, i1, j1 = inst

    f = cmdmap[cmd]

    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            lights[i, j] = f(lights[i, j])


def q_1(instructions):
    lights = {(i, j): False for i in range(1000) for j in range(1000)}

    cmdmap = {
        'turn on': lambda x: True,
        'turn off': lambda x: False,
        'toggle': lambda x: not x,
    }

    for inst in instructions:
        update_lights(lights, inst, cmdmap)

    return sum(lights.values())


def q_2(instructions):
    lights = {(i, j): 0 for i in range(1000) for j in range(1000)}

    cmdmap = {
        'turn on': lambda x: x + 1,
        'turn off': lambda x: max(0, x - 1),
        'toggle': lambda x: x + 2,
    }

    for inst in instructions:
        update_lights(lights, inst, cmdmap)

    return sum(lights.values())


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 6 ########################################################"
    instructions = load_instructions()
    print "\tquestion 1 answer: {}".format(q_1(instructions))
    print "\tquestion 2 answer: {}".format(q_2(instructions))
