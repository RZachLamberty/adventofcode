#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day5.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 9 puzzles for the advent of codec (adventofcode.com/2017/day/9)

Usage:
    <usage>

"""

import collections
import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = [
    ['{}', 1],
    ['{{{}}}', 6],
    ['{{},{}}', 5],
    ['{{{},{},{{}}}}', 16],
    ['{<a>,<a>,<a>,<a>}', 1],
    ['{{<ab>},{<ab>},{<ab>},{<ab>}}', 9],
    ['{{<!!>},{<!!>},{<!!>},{<!!>}}', 9],
    ['{{<a!>},{<a!>},{<a!>},{<ab>}}', 3],
]
TEST_2 = [
    ['<>', 0],
    ['<random characters>', 17],
    ['<<<<>', 3],
    ['<{!>}>', 2],
    ['<!!>', 0],
    ['<!!!>>', 0],
    ['<{o"i!a,<{i<a>', 10],
]

FNAME = os.path.join('data', 'day9.txt')
LOGGER = logging.getLogger('day9')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def clean_ignores(s):
    return re.sub('!.', '', s)


def clean_garbage(s, counts=False):
    foo = re.subn if counts else re.sub
    return foo('<[^>]*>', '', s)


def test_garbage():
    assert clean_garbage(clean_ignores('<>')) == ''
    assert clean_garbage(clean_ignores('<random characters>')) == ''
    assert clean_garbage(clean_ignores('<<<<>')) == ''
    assert clean_garbage(clean_ignores('<{!>}>')) == ''
    assert clean_garbage(clean_ignores('<!!>')) == ''
    assert clean_garbage(clean_ignores('<!!!>>')) == ''
    assert clean_garbage(clean_ignores('<{o"i!a,<{i<a>')) == ''


def parse_line(s):
    s = clean_garbage(clean_ignores(s))
    level = 0
    tot = 0
    for char in s:
        if char == '{':
            level += 1
        elif char == '}':
            tot += level
            level -= 1
    return tot


def test_parse_line():
    for (s, v) in TEST:
        LOGGER.debug('{}: {}'.format(v, s))
        assert parse_line(s) == v


def q_1(data):
    return sum(parse_line(s) for s in data)


def test_q_1():
    streams = [s for (s, v) in TEST]
    assert q_1(streams) == sum(v for (s, v) in TEST)


def count_garbage(s):
    si = clean_ignores(s)
    sg, ct = clean_garbage(si, counts=True)
    return len(si) - len(sg) - 2 * ct


def test_count_garbage():
    for (s, v) in TEST_2:
        LOGGER.debug('{}: {}'.format(v, s))
        assert count_garbage(s) == v


def q_2(s):
    return sum(count_garbage(_) for _ in s)


def test_q_2():
    streams = [s for (s, v) in TEST_2]
    assert q_2(streams) == sum(v for (s, v) in TEST_2)


def test():
    test_garbage()
    test_parse_line()
    test_q_1()
    test_count_garbage()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 9')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
