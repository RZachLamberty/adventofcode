#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day7.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 7 puzzles for the advent of code (adventofcode.com/day/7)

Usage:
    <usage>

"""

import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day7_input.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_instructions(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]


def smart_load(k, circuit):
    """ k could be a key of circuit or an integer; try integer first """
    try:
        return int(k)
    except ValueError:
        return circuit[k]


def and_command(circuit, inst):
    in1, in2, out = re.search(r'(\w+) AND (\w+) -> (\w+)', inst).groups()

    # in1 and in2 could be ints; try to load the text nodes and then try
    # to retun the int values
    circuit[out] = smart_load(in1, circuit) & smart_load(in2, circuit)


def or_command(circuit, inst):
    in1, in2, out = re.search(r'(\w+) OR (\w+) -> (\w+)', inst).groups()
    circuit[out] = circuit[in1] | circuit[in2]


def lshift_command(circuit, inst):
    in1, n, out = re.search(r'(\w+) LSHIFT (\w+) -> (\w+)', inst).groups()
    circuit[out] = circuit[in1] << int(n)


def rshift_command(circuit, inst):
    in1, n, out = re.search(r'(\w+) RSHIFT (\d) -> (\w+)', inst).groups()
    circuit[out] = circuit[in1] >> int(n)


def not_command(circuit, inst):
    in1, out = re.search(r'NOT (\w+) -> (\w+)', inst).groups()
    circuit[out] = ~circuit[in1]


def assign_command(circuit, inst):
    in1, out = re.match(r'(\w+) -> (\w+)', inst).groups()
    circuit[out] = smart_load(in1, circuit)


def update_circuit(circuit, inst):
    if 'AND' in inst:
        f = and_command
    elif 'LSHIFT' in inst:
        f = lshift_command
    elif 'RSHIFT' in inst:
        f = rshift_command
    elif 'NOT' in inst:
        f = not_command
    elif 'OR' in inst:
        f = or_command
    else:
        f = assign_command

    f(circuit, inst)


def only_pos_circuit_values(circuit):
    for (k, v) in circuit.items():
        if v < 0:
            circuit[k] += 2**16


def q_1(instructions):
    circuit = {}

    instWithSuccess = {i: False for i in instructions}

    while not all(instWithSuccess.values()):
        for (inst, successful) in instWithSuccess.items():
            if not successful:
                try:
                    update_circuit(circuit, inst)
                    instWithSuccess[inst] = True
                except:
                    pass

        if circuit.get('a', False):
            break

    only_pos_circuit_values(circuit)
    return circuit['a']


def q_2(instructions):
    aval = q_1(instructions)

    bAssignInd = None
    for (i, inst) in enumerate(instructions):
        if inst.endswith('-> b'):
            instructions[i] = '{} -> b'.format(aval)

    return q_1(instructions)


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 7 ########################################################"
    instructions = load_instructions()
    print "\tquestion 1 answer: {}".format(q_1(instructions))
    print "\tquestion 2 answer: {}".format(q_2(instructions))
