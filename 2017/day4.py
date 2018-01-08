#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day4.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 4 puzzles for the advent of codec (adventofcode.com/2017/day/4)

Usage:
    <usage>

"""

import os

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day4.txt')
LOGGER = logging.getLogger('day4')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]


def validate_passphrase(p):
    words = p.split(' ')
    unique = set(words)
    return len(words) == len(unique)


def q_1(plist):
    return sum(validate_passphrase(p) for p in plist)


def test_q_1():
    assert validate_passphrase('aa bb cc dd ee')
    assert not validate_passphrase('aa bb cc dd aa')
    assert validate_passphrase('aa bb cc dd aaa')


def hypervalidate_passphrase(p):
    words = [''.join(sorted(word)) for word in p.split(' ')]
    unique = set(words)
    return len(words) == len(unique)


def q_2(plist):
    return sum(hypervalidate_passphrase(p) for p in plist)


def test_q_2():
    assert hypervalidate_passphrase('abcde fghij')
    assert not hypervalidate_passphrase('abcde xyz ecdab')
    assert hypervalidate_passphrase('a ab abc abd abf abj')
    assert hypervalidate_passphrase('iiii oiii ooii oooi oooo')
    assert not hypervalidate_passphrase('oiii ioii iioi iiio')


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 4')
    data = load_data()
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
