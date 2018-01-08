#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day21.py
Author: zlamberty
Created: 2017-12-23

Description:
    day 21 puzzles for the advent of codec (adventofcode.com/2017/day/21)

Usage:
    <usage>

"""

import os

import eri.logging as logging
import numpy as np

from utils import array_to_str, str_to_array


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

TEST = (
    2,
    """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
)
FNAME = os.path.join('data', 'day21.txt')
LOGGER = logging.getLogger('day21')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

class Pattern(object):
    def __init__(self, pattern, artbook):
        self.pattern = pattern
        self.artbook = artbook
        self.array = str_to_array(self.pattern)

    def __str__(self):
        return '\n'.join(
            self.pattern[self.size * i: self.size * (i + 1)]
            for i in range(self.size)
        )

    @property
    def size(self):
        return self.array.shape[0]

    def enhance(self):
        if self.size % 2 == 0:
            chunksize = 2
        elif self.size % 3 == 0:
            chunksize = 3
        else:
            raise ValueError("problem with the size of the array")

        numchunks = self.size // chunksize
        nextsize = (chunksize + 1) * numchunks
        a = np.zeros((nextsize, nextsize))
        for i in range(numchunks):
            for j in range(numchunks):
                chunk = self.array[
                    chunksize * i: chunksize * (i + 1),
                    chunksize * j: chunksize * (j + 1)
                ]
                chunkstr = array_to_str(chunk)
                replchunk = str_to_array(self.artbook[chunkstr])
                a[
                    (chunksize + 1) * i: (chunksize + 1) * (i + 1),
                    (chunksize + 1) * j: (chunksize + 1) * (j + 1)
                ] = replchunk
        self.array = a.copy()
        self.pattern = array_to_str(self.array)

    @property
    def array_mirrors(self):
        return [
            self.array,
            self.array[:, ::-1],
            self.array[::-1, :],
            self.array[::-1, ::-1],
            self.array.T,
            self.array[:, ::-1].T,
            self.array[::-1, :].T,
            self.array[::-1, ::-1].T,
        ]

    @property
    def str_mirrors(self):
        return {array_to_str(a) for a in self.array_mirrors}


def load_data(fname=FNAME):
    with open(fname, 'r') as fp:
        return 5, fp.read()


def make_artbook(insts):
    artbook = {}
    for inst in insts.splitlines():
        lhs, rhs = inst.replace('/', '').split(' => ')
        p = Pattern(lhs, None)
        artbook.update({_: rhs for _ in p.str_mirrors})
    return artbook


def q_1(data):
    n, insts = data
    artbook = make_artbook(insts)
    p = Pattern('.#...####', artbook)
    LOGGER.debug('\n{}'.format(p))
    for i in range(n):
        p.enhance()
        LOGGER.debug('\n{}'.format(p))
    return p.array.sum()


def test_q_1():
    assert q_1(TEST) == 12


def q_2(data):
    n, insts = data
    data = 18, insts
    return q_1(data)


def test_q_2():
    assert True


def test():
    test_q_1()
    test_q_2()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    LOGGER.warning('day 21')
    data = load_data()
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('question 1 answer: {}'.format(q_1(data)))
    LOGGER.info('question 2 answer: {}'.format(q_2(data)))
