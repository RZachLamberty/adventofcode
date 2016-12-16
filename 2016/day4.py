#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day4.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 4 puzzles for the advent of code (adventofcode.com/2016/day/4)

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

ALPHA = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_LEN = len(ALPHA)
FNAME = os.path.join('data', 'day4.txt')
logger = logging.getLogger('day4')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def parse_lines(data):
    for line in data:
        yield parse_line(line)


def parse_line(line):
    (name, sectorId, checksum) = re.match(
        '([^\d]+)\-(\d*)\[(.*)\]', line
    ).groups()
    return (name, int(sectorId), checksum)


def check_sum(name):
    x = collections.Counter(name.replace('-', ''))
    return ''.join(
        letter for letter in sorted(x.keys(), key=lambda k: (-x[k], k))[:5]
    )


def q_1(data):
    return sum(
        sectorId
        for (name, sectorId, checksum) in parse_lines(data)
        if check_sum(name) == checksum
    )


def test_q_1():
    assert q_1([
        'aaaaa-bbb-z-y-x-123[abxyz]',
        'a-b-c-d-e-f-g-h-987[abcde]',
        'not-a-real-room-404[oarel]',
        'totally-real-room-200[decoy]',
    ]) == 1514


def decrypt_name(name, sid):
    return ''.join(
        ' ' if char == '-' else ALPHA[(ALPHA.index(char) + sid) % ALPHA_LEN]
        for char in name
    )


def q_2(data):
    return [
        sectorId
        for (name, sectorId, checksum) in parse_lines(data)
        if check_sum(name) == checksum
        and decrypt_name(name, sectorId) == 'northpole object storage'
    ][0]


def test_q_2():
    assert decrypt_name('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 4')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
