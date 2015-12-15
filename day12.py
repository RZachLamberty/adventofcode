#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day12.py
Author: zlamberty
Created: 2015-12-09

Description:


Usage:
    <usage>

"""

import os
import re
import json


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day12.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_input(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read()


def q1(input):
    """ docstring """
    return sum(int(el) for el in re.findall(r'-*\d+', input))


def node_sum(d):
    """ sum of values in d, provided d does not have 'red' as a key """
    if isinstance(d, (int, float)):
        return d
    elif isinstance(d, dict):
        if 'red' in d or 'red' in d.values():
            return 0
        else:
            return sum(node_sum(v) for v in d.values())
    elif isinstance(d, basestring):
        return 0
    elif isinstance(d, list):
        return sum(node_sum(el) for el in d)
    else:
        print d
        print type(d)
        raise ValueError()


def q2(input):
    """ docstring """
    return node_sum(json.loads(input))




# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    input = load_input()
    print "the answer to q1: {}".format(q1(input))
    print "the answer to q2: {}".format(q2(input))
