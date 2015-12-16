#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day16.py
Author: zlamberty
Created: 2016-12-09

Description:
    day 16 puzzles for the advent of code (adventofcode.com/day/16)

Usage:
    <usage>

"""

import itertools
import os
import pandas as pd
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day16.txt')
RE = r'({}): (\d+)'.format('|'.join([
    'children', 'cats', 'samoyeds', 'pomeranians', 'akitas', 'vizslas',
    'goldfish', 'trees', 'cars', 'perfumes',
]))
RIGHT_AUNT = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_aunts(fname=FNAME):
    aunts = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            aunt = {}
            aunt['num'] = int(re.search(r'Sue (\d+)', line).groups()[0])
            aunt.update({k: int(v) for (k, v) in re.findall(RE, line)})
            aunts.append(aunt)

    return aunts


def q_1(aunts, rightAunt=RIGHT_AUNT):
    for aunt in aunts:
        if all(rightAunt[k] == v for (k, v) in aunt.items() if not k == 'num'):
            return aunt['num']


def comp_dicts(d1, d2):
    for (key, v) in d1.items():
        if key == 'num':
            continue
        elif key in ['cats', 'trees']:
            if v <= d2[key]:
                return False
        elif key in ['pomeranians', 'goldfish']:
            if v >= d2[key]:
                return False
        elif v != d2[key]:
            return False
    return True


def q_2(aunts, rightAunt=RIGHT_AUNT):
    for aunt in aunts:
        if comp_dicts(aunt, rightAunt):
            return aunt['num']


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 16 ########################################################"
    aunts = load_aunts()
    print "\tquestion 1 answer: {}".format(q_1(aunts))
    print "\tquestion 2 answer: {}".format(q_2(aunts))
