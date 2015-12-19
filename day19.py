#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day19.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 19 puzzles for the advent of code (adventofcode.com/day/19)

Usage:
    <usage>

"""

import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day19.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_info(fname=FNAME):
    repl = []
    input = None
    with open(fname, 'rb') as f:
        for line in f.readlines():
            try:
                a, b = re.search('(\w+) => (\w+)', line.strip()).groups()
                repl.append((a, b))
            except:
                if line.strip():
                    input = line.strip()
    return repl, input


def test_info():
    repl = [
        ['H', 'HO'],
        ['H', 'OH'],
        ['O', 'HH']
    ]
    input = 'HOH'
    return repl, input


def test_info_2():
    repl = [
        ['e', 'H'],
        ['e', 'O'],
        ['H', 'HO'],
        ['H', 'OH'],
        ['O', 'HH']
    ]
    input = 'e'
    return repl, input


def repl_strings(rep, input):
    s = set()
    i = input.find(rep[0])
    if i != -1:
        s.add(input.replace(rep[0], rep[1], 1))
        for replstr in repl_strings(rep, input[i + 1:]):
            s.add(input[:i + 1] + replstr)
    return s


def q_1(repl, input):
    return len({s for rep in repl for s in repl_strings(rep, input)})


def q_2(repl, input):
    reg = sum(el.isupper() for el in input)
    paren = input.count('Rn') + input.count('Ar')
    com = input.count('Y')
    return reg - paren - 2 * com - 1


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 19 ########################################################"
    repl, input = load_info()
    print "\tquestion 1 answer: {}".format(q_1(repl, input))
    print "\tquestion 2 answer: {}".format(q_2(repl, input))
