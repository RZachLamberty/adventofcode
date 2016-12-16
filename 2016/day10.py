#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day10.py
Author: zlamberty
Created: 2016-12-02

Description:
    day 10 puzzles for the advent of code (adventofcode.com/2016/day/10)

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

FNAME = os.path.join('data', 'day10.txt')
logger = logging.getLogger('day10')
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_data(fname=FNAME):
    with open(fname, 'r') as f:
        return [line.strip() for line in f]


def read_instructions(data):
    inits = []
    rules = []
    for instruction in data:
        if instruction[:3] == 'bot':
            botId, lowDst, lowId, highDst, highId = re.match(
                'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)',
                instruction
            ).groups()
            rules.append({
                'botId': int(botId),
                'lowDst': lowDst,
                'lowId': int(lowId),
                'highDst': highDst,
                'highId': int(highId)
            })
        elif instruction[:5] == 'value':
            chipNum, botNum = map(
                int,
                re.match('value (\d+) goes to bot (\d+)', instruction).groups()
            )
            inits.append({'chipNum': chipNum, 'botNum': botNum})
        else:
            ValueError("unable to assign instruction '{}'".format(instruction))
    return inits, rules


def init_bots(inits):
    bots = collections.defaultdict(set)
    for init in inits:
        bots[init['botNum']].add(init['chipNum'])
    return bots


def apply_rule(bots, output, rule):
    botId = rule['botId']
    botChips = bots[botId]
    if len(botChips) == 2:
        low, high = sorted(botChips)

        lowDstDict = bots if rule['lowDst'] == 'bot' else output
        lowDstDict[rule['lowId']].add(low)

        highDstDict = bots if rule['highDst'] == 'bot' else output
        highDstDict[rule['highId']].add(high)


def bot_would_compare(bots, comps):
    compset = set(comps)
    for (k, v) in bots.items():
        if compset == v:
            return k
    return None


def q_1(data, comps=(17, 61)):
    """find the bot which, given instructions in data, compares the two
    microchips with values in comps

    """
    inits, rules = read_instructions(data)
    bots = init_bots(inits)
    output = collections.defaultdict(set)

    while True:
        for rule in rules:
            apply_rule(bots, output, rule)

            botId = bot_would_compare(bots, comps)
            if botId:
                return botId


def test_q_1():
    assert q_1([
        'value 5 goes to bot 2',
        'bot 2 gives low to bot 1 and high to bot 0',
        'value 3 goes to bot 1',
        'bot 1 gives low to output 1 and high to bot 0',
        'bot 0 gives low to output 2 and high to output 0',
        'value 2 goes to bot 2',
    ], comps=(2, 5)) == 2


def q_2(data):
    inits, rules = read_instructions(data)
    bots = init_bots(inits)
    output = collections.defaultdict(set)

    while True:
        for rule in rules:
            apply_rule(bots, output, rule)

        try:
            return list(output[0])[0] * list(output[1])[0] * list(output[2])[0]
        except:
            pass


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    logger.warning('day 10')
    data = load_data()
    logger.info('question 1 answer: {}'.format(q_1(data)))
    logger.info('question 2 answer: {}'.format(q_2(data)))
