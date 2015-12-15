#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day15.py
Author: zlamberty
Created: 2015-12-09

Description:
    day 15 puzzles for the advent of code (adventofcode.com/day/15)

Usage:
    <usage>

"""

import os
import re

from collections import Counter


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

FNAME = os.path.join('data', 'day15.txt')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_ingredients(fname=FNAME):
    ingredients = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            try:
                i, cap, dur, flav, text, cal = re.match(
                    r'(\w+): capacity ([-\d]+), durability ([-\d]+), flavor ([-\d]+), texture ([-\d]+), calories ([-\d]+)',
                    line.strip()
                ).groups()
                ingredients[i] = {
                    'capacity': int(cap),
                    'durability': int(dur),
                    'flavor': int(flav),
                    'texture': int(text),
                    'calories': int(cal)
                }
            except:
                pass

    return pd.DataFrame(ingredients)


def cookie_score(recipe, ingredients):
    score = defaultdict(int)
    for (ing, tsp) in recipe.items():
        for (qual, val) in ingredients[ing].items():
            score[qual] += val * tsp


def recipes(ings):
    pass


def q_1(ingredients):
    return max(
        cookie_score(recipe, ingredients)
        for recipe in recipes(ingredients.keys)
    )


def q_2(ingredients):
    return Counter(
        max(
            ingredients,
            key=lambda r: dist_at_t(
                ingredients[r][0], ingredients[r][1], ingredients[r][2], i
            )
        ) for i in range(1, 2504)
    )


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 15 ########################################################"
    ingredients = load_ingredients()
    print "\tquestion 1 answer: {}".format(q_1(ingredients))
    print "\tquestion 2 answer: {}".format(q_2(ingredients))
