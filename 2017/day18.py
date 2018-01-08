#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day18.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 18 puzzles for the advent of codec (adventofcode.com/2017/day/18)

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

TEST = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
TEST_2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""
FNAME = os.path.join('data', 'day18.txt')
LOGGER = logging.getLogger('day18')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_instruction(inst):
    foo, args = re.match('(snd|set|add|mul|mod|rcv|jgz) (.+)', inst).groups()
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

    if foo == 'snd':
        reg['last_played'] = reg_or_int(x, reg)
    elif foo == 'set':
        reg[x] = reg_or_int(y, reg)
    elif foo == 'add':
        reg[x] += reg_or_int(y, reg)
    elif foo == 'mul':
        reg[x] *= reg_or_int(y, reg)
    elif foo == 'mod':
        reg[x] %= reg_or_int(y, reg)
    elif foo == 'rcv':
        if reg_or_int(x, reg):
            return reg['last_played']
    elif foo == 'jgz':
        if reg_or_int(x, reg) > 0:
            reg['jump'] = reg_or_int(y, reg)
    else:
        raise ValueError("improper instruction: {}".format(inst))


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
    return rcv


def test_q_1():
    assert q_1(TEST) == 4


def run_program(register, queue_in, queue_out, commands):
    while 0 <= register["counter"] < len(commands):
        foo, args = commands[register["counter"]]

        try:
            x, y = args
        except ValueError:
            x = args[0]

        if foo == "rcv":
            if len(queue_in) == 0:
                return True
            register[x] = queue_in.popleft()
        if foo == "jgz":
            if reg_or_int(x, register) > 0:
                register["counter"] += reg_or_int(y, register)
                continue
        if foo == "snd":
            queue_out.append(reg_or_int(x, register))
            register["sent"] = reg_or_int("sent", register) + 1
        if foo == "set":
            register[x] = reg_or_int(y, register)
        if foo == "add":
            register[x] = reg_or_int(x, register) + reg_or_int(y, register)
        if foo == "mul":
            register[x] = reg_or_int(x, register) * reg_or_int(y, register)
        if foo == "mod":
            register[x] = reg_or_int(x, register) % reg_or_int(y, register)
        register["counter"]+=1
    return False


def q_2(data):
    insts = [parse_instruction(inst) for inst in data.splitlines()]
    reg0 = {'p': 0, 'counter': 0, 'sent': 0}
    reg1 = {'p': 1, 'counter': 0, 'sent': 0}
    q0 = collections.deque()
    q1 = collections.deque()

    while True:
        if not run_program(reg0, q0, q1, insts):
            break
        if not run_program(reg1, q1, q0, insts):
            break
        if len(q0) == 0 and len(q1) == 0:
            break

    return reg0['sent']


def test_q_2():
    assert q_2(TEST_2) == 3


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 18')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
