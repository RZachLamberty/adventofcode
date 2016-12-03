#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day18.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 18 puzzles for the advent of code (adventofcode.com/day/18)

Usage:
    <usage>

"""

import numpy as np
import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day18.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_grid(fname=FNAME):
    """ docstring """
    with open(fname, 'rb') as f:
        x = [
            [int(el) for el in line.strip().replace('#', '1').replace('.', '0')]
            for line in f.readlines()
        ]
    return np.array(x)


def test_grid():
    return np.array([
        [0, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 0]
    ])


def update_grid(grid, pincorners=False):
    new = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        imin = max(0, i - 1)
        imax = min(i + 1, grid.shape[0])
        for j in range(grid.shape[1]):
            oldval = grid[i, j]
            jmin = max(0, j - 1)
            jmax = min(j + 1, grid.shape[1])
            onNeighbs = grid[imin:imax + 1, jmin:jmax + 1].sum() - oldval
            if oldval == 1:
                new[i, j] = int(onNeighbs in [2, 3])
            else:
                new[i, j] = int(onNeighbs == 3)

    if pincorners:
        new[0, 0] = 1
        new[0, grid.shape[1]-1] = 1
        new[grid.shape[0]-1, 0] = 1
        new[grid.shape[0]-1, grid.shape[1] - 1] = 1
    return new


def q_1(grid):
    for i in range(100):
        grid = update_grid(grid)
    return grid.sum()


def q_2(grid):
    for i in range(100):
        grid = update_grid(grid, pincorners=True)
    return grid.sum()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 18 ########################################################"
    grid = load_grid()
    print "\tquestion 1 answer: {}".format(q_1(grid))
    print "\tquestion 2 answer: {}".format(q_2(grid))
