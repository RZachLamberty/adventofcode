#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day21.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 21 puzzles for the advent of code (adventofcode.com/day/21)

Usage:
    <usage>

"""

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

BOSS = {
    'hit_points': 103,
    'damage': 9,
    'armor': 2,
}

WEAPONS = {
    'dagger': {'cost': 8, 'damage': 4, 'armor': 0},
    'shortsword': {'cost': 10, 'damage': 5, 'armor': 0},
    'warhammer': {'cost': 25, 'damage': 6, 'armor': 0},
    'longsword': {'cost': 40, 'damage': 7, 'armor': 0},
    'greataxe': {'cost': 74, 'damage': 8, 'armor': 0},
}
ARMOR = {
    'leather': {'cost': 13, 'damage': 0, 'armor': 1},
    'chainmail': {'cost': 31, 'damage': 0, 'armor': 2},
    'splintmail': {'cost': 53, 'damage': 0, 'armor': 3},
    'bandedmail': {'cost': 75, 'damage': 0, 'armor': 4},
    'platemail': {'cost': 102, 'damage': 0, 'armor': 5},
}
RINGS = {
    'damage_1': {'cost': 25, 'damage': 1, 'armor': 0},
    'damage_2': {'cost': 50, 'damage': 2, 'armor': 0},
    'damage_3': {'cost': 100, 'damage': 3, 'armor': 0},
    'defense_1': {'cost': 20, 'damage': 0, 'armor': 1},
    'defense_2': {'cost': 40, 'damage': 0, 'armor': 2},
    'defense_3': {'cost': 80, 'damage': 0, 'armor': 3},
}

# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_boss():
    return BOSS


def test_player():
    return {
        'armor': 5,
        'damage': 5,
        'hit_points': 8
    }

def test_boss():
    return {
        'armor': 2,
        'damage': 7,
        'hit_points': 12
    }


def equipment():
    for w in WEAPONS.keys():
        for a in [None] + ARMOR.keys():
            for r1 in [None] + RINGS.keys():
                for r2 in [None] + RINGS.keys():
                    if r1 != r2 or (r1 is None and r2 is None):
                        yield w, a, r1, r2


def equipment_stats(equip):
    w, a, r1, r2 = equip
    return {
        key: (
            WEAPONS[w][key]
            + ARMOR.get(a, {}).get(key, 0)
            + RINGS.get(r1, {}).get(key, 0)
            + RINGS.get(r2, {}).get(key, 0)
        )
        for key in ['cost', 'damage', 'armor']
    }


def wins_battle(player, boss):
    phit = player['hit_points']
    bhit = boss['hit_points']
    playerdam = max(1, player['damage'] - boss['armor'])
    bossdam = max(1, boss['damage'] - player['armor'])
    while True:
        bhit -= playerdam
        if bhit <= 0:
            return True
        phit -= bossdam
        if phit <= 0:
            return False


def q_1(boss=BOSS):
    mincost = None
    for equip in equipment():
        player = equipment_stats(equip)
        player['hit_points'] = 100
        if wins_battle(player, boss):
            if (mincost is None):
                mincost = player['cost']
            else:
                mincost = min(mincost, player['cost'])
    return mincost


def q_2(boss):
    maxcost = None
    for equip in equipment():
        player = equipment_stats(equip)
        player['hit_points'] = 100
        if not wins_battle(player, boss):
            if (maxcost is None):
                maxcost = player['cost']
            else:
                maxcost = max(maxcost, player['cost'])
    return maxcost


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 21 ########################################################"
    boss = load_boss()
    print "\tquestion 1 answer: {}".format(q_1(boss))
    print "\tquestion 2 answer: {}".format(q_2(boss))
