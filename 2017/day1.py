#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day1.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 1 puzzles for the advent of codec (adventofcode.com/2017/day/1)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day01.txt')
LOGGER = logging.getLogger('day1')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return f.read().strip()


def q_1(captcha):
    return sum([
        int(n)
        for (i, n) in enumerate(captcha)
        if n == captcha[(i + 1) % len(captcha)]
    ])


def test_q_1():
    assert q_1('1122') == 3
    assert q_1('1111') == 4
    assert q_1('1234') == 0
    assert q_1('91212129') == 9


def q_2(captcha):
    delta = len(captcha) // 2
    return sum([
        int(n)
        for (i, n) in enumerate(captcha)
        if n == captcha[(i + delta) % len(captcha)]
    ])


def test_q_2():
    assert q_2('1212') == 6
    assert q_2('1221') == 0
    assert q_2('123425') == 4
    assert q_2('123123') == 12
    assert q_2('12131415') == 4


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 1')
    data = load_data()
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
