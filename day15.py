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

import itertools
import os
import pandas as pd
import re


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

    return pd.DataFrame(ingredients)


def cookie_score(recipe, ingredients, calGoal=None):
    s = ingredients * recipe
    if calGoal and s.loc['calories'].sum() != calGoal:
        return 0
    s = s.drop('calories').sum(axis=1)
    s[s < 0] = 0
    return s.prod()


def recipes(ingredients):
    for perm in itertools.product(range(101), repeat=ingredients.shape[1] - 1):
        l = 100 - sum(perm)
        if l >= 0:
            yield perm + (l,)


def test_ingredients():
    return pd.DataFrame({
        'Butterscotch': {'capacity': -1, 'durability': -2, 'flavor': 6, 'texture': 3, 'calories': 8},
        'Cinnamon': {'capacity': 2, 'durability': 3, 'flavor': -2, 'texture': -1, 'calories': 3},
    })


def tests():
    ingredients = test_ingredients()
    assert cookie_score((44, 56), ingredients) == 62842880
    assert q_1(ingredients) == 62842880
    assert cookie_score((40, 60), ingredients, calGoal=500) == 57600000
    assert q_2(ingredients) == 57600000


def q_1(ingredients):
    return max(
        cookie_score(recipe, ingredients)
        for recipe in recipes(ingredients)
    )


def q_2(ingredients):
    return max(
        cookie_score(recipe, ingredients, calGoal=500)
        for recipe in recipes(ingredients)
    )


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 15 ########################################################"
    ingredients = load_ingredients()
    print "\tquestion 1 answer: {}".format(q_1(ingredients))
    print "\tquestion 2 answer: {}".format(q_2(ingredients))
