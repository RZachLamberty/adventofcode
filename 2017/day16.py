#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day16.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 16 puzzles for the advent of codec (adventofcode.com/2017/day/16)

Usage:
    <usage>

"""

import functools
import os
import string

import eri.logging as logging
import tqdm


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day16.txt')
LOGGER = logging.getLogger('day16')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return string.ascii_lowercase[:16], f.read().strip()


def apply_dance(dance, progs):
    LOGGER.debug(dance)
    if dance[0] == 's':
        size = int(dance[1:])
        newprogs = progs[-size:] + progs[:-size]
    elif dance[0] in ['x', 'p']:
        if dance[0] == 'x':
            i0, i1 = dance[1:].split('/')
            p0 = progs[int(i0)]
            p1 = progs[int(i1)]
        elif dance[0] == 'p':
            p0, p1 = dance[1:].split('/')

        newprogs = progs
        newprogs = newprogs.replace(p0, '!')
        newprogs = newprogs.replace(p1, p0)
        newprogs = newprogs.replace('!', p1)
    else:
         raise ValueError('improper dance instruction: {}'.format(dance))
    LOGGER.debug('{} --> {}'.format(progs, newprogs))
    return newprogs


def test_apply_dance():
    assert apply_dance('s3', 'abcde') == 'cdeab'
    assert apply_dance('s1', 'abcde') == 'eabcd'
    assert apply_dance('x3/4', 'eabcd') == 'eabdc'
    assert apply_dance('pe/b', 'eabdc') == 'baedc'


@functools.lru_cache(maxsize=None)
def q_1(data):
    progs, dancestr = data
    for dance in dancestr.split(','):
        progs = apply_dance(dance, progs)
    return progs


def test_q_1():
    assert q_1(('abcde', 's1,x3/4,pe/b')) == 'baedc'


def q_2(data):
    progstr, dancestr = data
    orig_progs = progstr

    for i in tqdm.trange(int(1e9)):
        progs = q_1(data)
        data = progs, dancestr

    return progs


def test_q_2():
    assert True


def test():
    test_apply_dance()
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 16')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
