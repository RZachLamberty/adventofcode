#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day8.py
Author: zlamberty
Created: 2015-12-08

Description:
    day 8 puzzles for the advent of code (adventofcode.com/day/8)

Usage:
    <usage>

"""

import os


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day8_input.txt')
TEST_FNAME = os.path.join('data', 'day8_test.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_codestrings(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]


def decode_len(s):
    # super easy mode:
    return len(eval(s))
    i = 0
    l = len(s)
    skip = 0
    while i < l - 1:
        currchar = s[i]
        nextchar = s[i + 1]

        if currchar == '\\':
            if nextchar == '\\':
                # skip the next char
                skip += 1
                i += 1
            elif nextchar == '"':
                # skip the next char
                skip += 1
                i += 1
            elif nextchar == 'x':
                # skip the next three chars
                skip += 3
                i += 3

        i += 1
    # open and close quotes yield 2 other skippers
    return l - skip - 2


def encode_len(s):
    return (
        len(s)  # original code length
        + s.count('"')
        + s.count('\\')
        + 2  # open and close quotes
    )


def q_1(codestrings):
    codenum = sum(len(s) for s in codestrings)
    charnum = sum(decode_len(s) for s in codestrings)

    return codenum - charnum


def q_2(codestrings):
    codenum = sum(len(s) for s in codestrings)
    charnum = sum(encode_len(s) for s in codestrings)

    return charnum - codenum


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 8 ########################################################"
    codestrings = load_codestrings()
    print "\tquestion 1 answer: {}".format(q_1(codestrings))
    print "\tquestion 2 answer: {}".format(q_2(codestrings))
