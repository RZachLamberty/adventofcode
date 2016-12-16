#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day8.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 8 puzzles for the advent of code (adventofcode.com/2016/day/8)

Usage:
    <usage>

"""

import os
import re

import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day8.txt')
logger = logging.getLogger('day8')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def rect(arr, A, B):
    arr[:B, :A] = 1


def rotate_row(arr, A, B):
    arr[A, :] = list(arr[A, -B:]) + list(arr[A, : -B])


def rotate_column(arr, A, B):
    arr[:, A] = list(arr[-B:, A]) + list(arr[: -B, A])


def apply_instruction(arr, instruction):
    m = re.match('rect (\d+)x(\d+)', instruction)
    if m:
        (A, B) = m.groups()
        A = int(A)
        B = int(B)
        rect(arr, A, B)
        return

    m = re.match('rotate row y=(\d+) by (\d+)', instruction)
    if m:
        (A, B) = m.groups()
        A = int(A)
        B = int(B)
        rotate_row(arr, A, B)
        return

    m = re.match('rotate column x=(\d+) by (\d+)', instruction)
    if m:
        (A, B) = m.groups()
        A = int(A)
        B = int(B)
        rotate_column(arr, A, B)
        return

    raise ValueError('unparsed instruction: {}'.format(instruction))


def q_1(data):
    arr = sp.zeros((6, 50))

    for instruction in data:
        apply_instruction(arr, instruction)

    global ARR
    ARR = arr
    return arr.sum()


def test_q_1():
    assert q_1([
        'rect 3x2',
        'rotate column x=1 by 1',
        'rotate row y=0 by 4',
        'rotate column x=1 by 1',
    ]) == 6


def q_2(data):
    plt.matshow(ARR)
    plt.show()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 8')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
