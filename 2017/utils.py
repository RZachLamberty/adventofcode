#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: utils.py
Author: zlamberty
Created: 2017-12-26

Description:
    re-used utilities

Usage:
    <usage>

"""

import eri.logging as logging
import numpy as np

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

LOGGER = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   knot hash                   #
# ----------------------------- #

def apply_lengths(l, lengths, currpos, skip):
    n = len(l)
    for length in lengths:
        i0 = currpos
        i1 = (currpos + length - 1) % n
        newl = list(l)
        for i in range(length):
            newl[i1] = l[i0]
            newl[i0] = l[i1]
            i0 += 1
            i0 %= n
            i1 -= 1
            i1 %= n
        l = newl
        currpos += length + skip
        currpos %= n
        skip += 1
    return l, currpos, skip


def xor(l):
    res = 0
    for el in l:
        res ^= el
    return res


def test_xor():
    assert xor([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]) == 64


def dense_to_hex(l):
    return ''.join(['{:02x}'.format(_) for _ in l])


def knot_hash(data):
    skip = currpos = 0
    n, lengthstr = data
    # lengthstr to lengths
    lengths = [ord(_) for _ in lengthstr] + [17, 31, 73, 47, 23]
    l = list(range(n))

    for i in range(64):
        l, currpos, skip = apply_lengths(l, lengths, currpos, skip)

    # dense hash
    dh = [
        xor(l[16 * i: 16 * (i + 1)])
        for i in range(16)
    ]

    return dense_to_hex(dh)


def knot_hash_to_bin(kh):
    return ''.join(['{:04b}'.format(int(char, 16)) for char in kh])


# ----------------------------- #
#   str to array stuff          #
# ----------------------------- #

def str_to_array(s):
    l = len(s)
    n = int(l ** .5)
    a = np.array([0 if _ == '.' else 1 for _ in s])
    return a.reshape((n, n))


def array_to_str(a):
    return ''.join(
        '.' if elem == 0 else '#'
        for elem in a.flatten()
    )


def aoc_array_str(a):
    return '\n'.join([
        ''.join([
            '#' if elem else '.'
            for elem in row
        ])
        for row in a
    ])
