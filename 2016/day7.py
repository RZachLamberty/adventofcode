#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day17.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 17 puzzles for the advent of code (adventofcode.com/2016/day/17)

Usage:
    <usage>

"""

import os
import re

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day17.txt')
logger = logging.getLogger('day17')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def parse_ip(ip):
    subips = []
    hypernets = []
    for (i, s) in enumerate(ip.replace('[', ']').split(']')):
        if i % 2:
            hypernets.append(s)
        else:
            subips.append(s)
    return subips, hypernets


def supports_tls(ip):
    subips, hypernets = parse_ip(ip)
    if any(has_abba(hypernet) for hypernet in hypernets):
        return False

    if any(has_abba(subip) for subip in subips):
        return True

    return False


def has_abba(ip):
    for i in range(2, len(ip) - 1):
        if (ip[i] != ip[i + 1]) and (ip[i: i + 2] == ip[i - 1] + ip[i - 2]):
            return True
    return False


def q_1(data):
    return sum([supports_tls(ip) for ip in data])


def test_q_1():
    assert q_1([
        'abba[mnop]qrst',
        'abcd[bddb]xyyx',
        'aaaa[qwer]tyui',
        'ioxxoj[asdfgh]zxcvbn',
    ]) == 2


def get_abas(ips):
    x = []
    for ip in ips:
        for i in range(len(ip) - 2):
            x0, x1, x2 = ip[i: i + 3]
            if x0 != x1 and x0 == x2:
                x.append(x0 + x1 + x2)
    return x


def bab_from_aba(aba):
    x0, x1, x2 = aba
    return x1 + x0 + x1


def supports_ssl(ip):
    subips, hypernets = parse_ip(ip)
    abas = get_abas(subips)

    for aba in abas:
        bab = bab_from_aba(aba)
        if any(bab in hypernet for hypernet in hypernets):
            return True

    return False


def q_2(data):
    return sum([supports_ssl(ip) for ip in data])


def test_q_2():
    assert q_2([
        'aba[bab]xyz',
        'xyx[xyx]xyx',
        'aaa[kek]eke',
        'zazbz[bzb]cdb',
    ]) == 3


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 17')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
