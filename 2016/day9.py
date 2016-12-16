#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day9.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 9 puzzles for the advent of code (adventofcode.com/2016/day/9)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day9.txt')
logger = logging.getLogger('day9')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def decompress(s):
    i = 0
    sout = ''
    while i < len(s):
        if s[i] == '(':
            # opening an instruction, parse it
            m = re.search('\((\d+)x(\d+)\)', s[i:])
            if m is None:
                raise ValueError("unable to parse string '{}...'".format(s[i: i + 20]))
            l, n = map(int, m.groups())
            i += m.end()

            # grab the next l characters and add them to sout n times; incr. i
            toadd = s[i: i + l]
            sout += toadd * n
            i += l
        else:
            sout += s[i]
            i += 1
    return sout


def q_1(data):
    return len(decompress(data))


def test_q_1():
    assert q_1('ADVENT') == 6
    assert q_1('A(1x5)BC') == 7
    assert q_1('(3x3)XYZ') == 9
    assert q_1('A(2x2)BCD(2x2)EFG') == 11
    assert q_1('(6x1)(1x3)A') == 6
    assert q_1('X(8x2)(3x3)ABCY') == 18


def decompression_length_v2(s):
    i = 0
    dl = 0
    while i < len(s):
        if s[i] == '(':
            # opening an instruction, parse it
            m = re.search('\((\d+)x(\d+)\)', s[i:])
            if m is None:
                raise ValueError("unable to parse string '{}...'".format(s[i: i + 20]))
            l, n = map(int, m.groups())
            i += m.end()

            # grab the next l characters and add them to sout n times; incr. i
            toadd = decompression_length_v2(s[i: i + l])
            dl += toadd * n
            i += l
        else:
            dl += 1
            i += 1
    return dl


def q_2(data):
    return decompression_length_v2(data)


def test_q_2():
    assert q_2('(3x3)XYZ') == 9
    assert q_2('X(8x2)(3x3)ABCY') == 20
    assert q_2('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
    assert q_2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 9')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
