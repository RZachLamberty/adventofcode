#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day23.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 23 puzzles for the advent of code (adventofcode.com/2016/day/23)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST_DATA = (
    [
    'cpy 2 a',
        'tgl a',
        'tgl a',
        'tgl a',
        'cpy 1 a',
        'dec a',
        'dec a',
    ],
    0,
    'a'
)

FNAME = os.path.join('data', 'day23.txt')
logger = logging.getLogger('day23')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    a0 = 7
    outregister = 'a'
    with open(fname, 'r') as f:
        return ([line.strip() for line in f], a0, outregister)


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


class AssembunnyComputer(object):
    def __init__(self, instructions, a=0, b=0, c=0, d=0, debug=False):
        self.instructions = instructions
        self.numInstructions = len(self.instructions)
        self.instructionPtr = 0
        self.reg = {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
        }
        self.debug = debug

        if self.debug:
            logging.getLogger('day23').setLevel(logging.DEBUG)
        else:
            logging.getLogger('day23').setLevel(logging.INFO)

    def is_done(self):
        return self.instructionPtr >= self.numInstructions

    def apply_instruction(self):
        # handle common command sequences first
        try:
            com0, a0 = self.instructions[self.instructionPtr]
            com1, a1 = self.instructions[self.instructionPtr + 1]
            com2, a2, b2 = self.instructions[self.instructionPtr + 2]
            isJumploop = all([
                com2 == 'jnz',
                b2 == -2,
                (
                    # move a1 to a0
                    ((com0, com1 == 'inc', 'dec') and (a1 == a2))
                    or
                    # move a0 to a1
                    ((com0, com1 == 'dec', 'inc') and (a0 == a2))
                )
            ])

            if isJumploop:
                # we will increase arg00 and decrease arg01 until arg01 is empty
                # this is equivalent to moving arg01 to arg00
                if com0 == 'inc':
                    incReg = a0
                    decReg = a1
                else:
                    incReg = a1
                    decReg = a0

                logger.debug(
                    "jumploop found! moving register {} to {}".format(
                        decReg, incReg
                    )
                )

                self.reg[incReg] += self.reg[decReg]
                self.reg[decReg] = 0
                self.instructionPtr += 3

                self.log_status()

                return
        except:
            pass

        # apply this one item and be done with it
        instruction = self.instructions[self.instructionPtr]

        logger.debug(instruction)

        com = instruction[0]
        increment = 1

        try:
            if com == 'cpy':
                x, y = instruction[1:]
                self.reg[y] = self.reg.get(x, x)
            elif com == 'inc':
                x = instruction[1]
                self.reg[x] += 1
            elif com == 'dec':
                x = instruction[1]
                self.reg[x] -= 1
            elif com == 'jnz':
                x, y = instruction[1:]
                if self.reg.get(x, x) != 0:
                    increment = self.reg.get(y, y)
            elif com == 'tgl':
                x = instruction[1]
                tglInstructionPtr = self.instructionPtr + self.reg.get(x, x)
                self.toggle_instruction(tglInstructionPtr)
        except Exception as e:
            logger.warning('failed to apply instruction: {}'.format(e))

        self.instructionPtr += increment

        self.log_status()

    def toggle_instruction(self, i):
        """'toggle' the instruction at index i"""
        try:
            com = self.instructions[i][0]
        except IndexError:
            logger.debug("invalid toggle index pointer, skipping")
            return

        if com == 'cpy':
            newcom = 'jnz'
        elif com == 'inc':
            newcom = 'dec'
        elif com == 'dec':
            newcom = 'inc'
        elif com == 'jnz':
            newcom = 'cpy'
        elif com == 'tgl':
            newcom = 'inc'

        if self.debug:
            logger.warning('toggling instruction {}'.format(self.instructions[i]))

        self.instructions[i][0] = newcom

        if self.debug:
            logger.warning('toggled to {}'.format(self.instructions[i]))
            input()

    def log_status(self):
        if self.debug:
            logger.debug('self.reg = {}'.format(self.reg))
            logger.debug('self.instructions = {}'.format(self.instructions))
            logger.debug('self.instructionPtr = {}'.format(self.instructionPtr))
            input()
        else:
            logger.info(self.reg)


def q_1(data):
    instructions, a0, outregister = data
    instructions = parse_instructions(instructions)
    ac = AssembunnyComputer(
        instructions=instructions,
        a=a0
    )

    while not ac.is_done():
        ac.apply_instruction()

    return ac.reg[outregister]


def test_q_1():
    assert q_1(TEST_DATA) == 3


def q_2(data, a0=12):
    data = data[0], a0, data[2]
    return q_1(data)


def test_q_2():
    assert q_2(None) == None


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 23')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
