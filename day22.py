#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: day22.py
Author: zlamberty
Created: 2015-12-17

Description:
    day 22 puzzles for the advent of code (adventofcode.com/day/22)

Usage:
    <usage>

"""

import collections
import itertools
import os
import re


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

LOSS, WIN = False, True


class ManaError(Exception):
    pass


class UncastableSpell(Exception):
    pass


class Spell(object):
    def __init__(self, cost=0, length=None, damage=None, heal=None, armor=None,
                 mana=None, verbose=False, **kwargs):
        self.cost = cost
        self.length = length
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.mana = mana
        self.verbose = verbose
        self.isActive = False

    def cast(self, player, boss, castSpells):
        self.isActive = True
        # can I cast this? Is it already active?
        sameActive = [
            spell
            for spellset in [player['spells'], castSpells]
            for spell in spellset
            if spell.__class__.__name__ == self.__class__.__name__
            and spell.isActive
        ]

        if any(sameActive):
            raise UncastableSpell()

        # mana casting cost
        player['mana'] -= self.cost
        player['mana_spent'] = player.get('mana_spent', 0) + self.cost
        if player['mana'] < 0:
            raise ManaError()

        self.myprint('player casts {}'.format(self.__class__.__name__))
        self.instant_effect(player, boss)

    def instant_effect(self, player, boss):
        pass

    def delayed_effect(self, player, boss):
        pass

    def myprint(self, el):
        if self.verbose:
            print el


class Missile(Spell):
    def __init__(self, verbose=False):
        super(Missile, self).__init__(cost=53, damage=4, verbose=verbose)

    def instant_effect(self, player, boss):
        self.myprint('  missile does {} damage to boss'.format(self.damage))
        boss['hit_points'] -= self.damage
        self.isActive = False


class Drain(Spell):
    def __init__(self, verbose=False):
        super(Drain, self).__init__(cost=73, damage=2, heal=2, verbose=verbose)

    def instant_effect(self, player, boss):
        self.myprint('drain does {} damage to boss and adds {} to player health'.format(self.damage, self.heal))
        boss['hit_points'] -= self.damage
        player['hit_points'] += self.heal
        self.isActive = False


class Shield(Spell):
    def __init__(self, verbose=False):
        super(Shield, self).__init__(cost=113, armor=7, length=6, verbose=verbose)
        self.counter = self.length

    def instant_effect(self, player, boss):
        self.myprint('shield increases armor by {}'.format(self.armor))
        player['armor'] = player.get('armor', 0) + self.armor

    def delayed_effect(self, player, boss):
        # leave if inactive
        if not self.isActive:
            return

        # activate
        # no activation

        # decrement
        self.counter -= 1
        self.myprint('  shield counter set to {}'.format(self.counter))

        # shut off if necessary
        if self.counter == 0:
            self.isActive = False
            player['armor'] = max(0, player.get('armor', 0) - self.armor)
            self.myprint(
                'shield phases out, armor decreases by {} to {}'.format(
                    self.armor,
                    player['armor']
                )
            )


class Poison(Spell):
    def __init__(self, verbose=False):
        super(Poison, self).__init__(cost=173, damage=3, length=6, verbose=verbose)
        self.counter = self.length

    def delayed_effect(self, player, boss):
        # leave if inactive
        if not self.isActive:
            return

        # activate
        if self.counter > 0:
            self.myprint('poison does {} damage to boss'.format(self.damage))
            boss['hit_points'] -= self.damage

        # decrement
        self.counter -= 1
        self.myprint('  poison counter set to {}'.format(self.counter))

        # shut off if necessary
        if self.counter == 0:
            self.isActive = False
            self.myprint('poison phases out')


class Recharge(Spell):
    def __init__(self, verbose=False):
        super(Recharge, self).__init__(cost=229, mana=101, length=5, verbose=verbose)
        self.counter = self.length

    def delayed_effect(self, player, boss):
        # leave if inactive
        if not self.isActive:
            return

        # activate
        if self.counter > 0:
            self.myprint('recharge adds {} to mana pool'.format(self.mana))
            player['mana'] += self.mana

        # decrement
        self.counter -= 1
        self.myprint('  mana counter set to {}'.format(self.counter))

        # shut off if necessary
        if self.counter == 0:
            self.isActive = False
            self.myprint('recharge phases out')


SPELLS = [Missile, Drain, Shield, Poison, Recharge]


def intlist_to_spelllist(intlist, verbose=False):
    return [SPELLS[i](verbose=verbose) for i in intlist]


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def load_stats():
    boss = {
        'hit_points': 51,
        'armor': 0,
        'damage': 9,
    }
    player = {
        'hit_points': 50,
        'armor': 0,
        'mana': 500,
    }
    return player, boss


def load_test_1():
    boss = {'hit_points': 13, 'damage': 8, 'armor': 0}
    player = {'hit_points': 10, 'mana': 250, 'armor': 0}
    player['spells'] = [
        Poison(verbose=True),
        Missile(verbose=True),
    ]
    return player, boss


def load_test_2():
    boss = {'hit_points': 14, 'damage': 8, 'armor': 0}
    player = {'hit_points': 10, 'mana': 250, 'armor': 0}
    player['spells'] = [
        Recharge(verbose=True),
        Shield(verbose=True),
        Drain(verbose=True),
        Poison(verbose=True),
        Missile(verbose=True),
    ]
    return player, boss


class NoMoreSpells(Exception):
    pass


def wins_battle(player, boss, verbose=False, bleeds=False):
    castSpells = []
    while True:
        if verbose:
            print '\n-- player turn'
            print '- player has {hit_points:} hit points, {armor:} armor, {mana:} mana'.format(**player)
            print '- boss has {hit_points:} hit points'.format(**boss)

        # player turn
        #  bleed out
        if bleeds:
            player['hit_points'] -= 1

        if player['hit_points'] <= 0:
            return LOSS

        #  effects
        for spell in castSpells:
            spell.delayed_effect(player, boss)
        if boss['hit_points'] <= 0:
            return WIN

        #  cast spells
        try:
            s = player['spells'].pop(0)
            s.cast(player, boss, castSpells)
            castSpells.append(s)
        except IndexError:
            raise NoMoreSpells()
        except ManaError:
            return LOSS
        except UncastableSpell:
            return LOSS

        if boss['hit_points'] <= 0:
            return WIN

        # boss turn
        if verbose:
            print '\n-- boss turn'
            print '- player has {hit_points:} hit points, {armor:} armor, {mana:} mana'.format(**player)
            print '- boss has {hit_points:} hit points'.format(**boss)

        #  effects
        for spell in castSpells:
            spell.delayed_effect(player, boss)
        if boss['hit_points'] <= 0:
            return WIN

        #  boss damage
        bossdam = max(1, boss['damage'] - player.get('armor', 0))
        if verbose:
            print 'Boss attacks for {} damage!'.format(bossdam)
        player['hit_points'] -= bossdam

        if player['hit_points'] <= 0:
            return LOSS

        if verbose:
            print ''


def test():
    # test 1
    player, boss = load_test_1()
    won = wins_battle(player, boss, verbose=True)

    print '\n*** SPENT {} to {}\n\n'.format(
        player['mana_spent'],
        'win' if won else 'lose',
    )

    # test 2
    player, boss = load_test_2()
    won = wins_battle(player, boss, verbose=True)

    print '\n*** SPENT {} to {}\n\n'.format(
        player['mana_spent'],
        'win' if won else 'lose',
    )


def f(prtrds=True, prtSubrds=False, verbose=False, bleeds=False):
    mincost = {}
    mincostspells = {}
    continueSpells = [[0], [1], [2], [3], [4]]
    i = 1
    while continueSpells:
        # next round -- for every previous valid set of spells, try adding
        # each of the spells to give us a new round.
        nextRoundSpells = []
        if prtrds:
            print 'starting spell round {} ({} options)'.format(
                i, len(continueSpells)
            )
        for (j, prevSpells) in enumerate(continueSpells):
            if prtSubrds:
                print '> sub-round {} out of {}'.format(j, len(continueSpells))
            for k in range(5):
                nowSpells = prevSpells + [k]
                player, boss = load_stats()
                player['spells'] = intlist_to_spelllist(nowSpells, verbose)

                try:
                    winner = wins_battle(player, boss, False, bleeds)
                    if winner:
                        # check against the all-time best
                        nowcost = player['mana_spent']
                        if (mincost is None) or nowcost < mincost:
                            mincost = nowcost
                            mincostspells = nowSpells
                except NoMoreSpells:
                    # game didn't end with the number of spells we had, this is
                    # a valid continuing spell set if it costs less than the
                    # current all-time best
                    if (mincost is None) or player['mana_spent'] < mincost:
                        nextRoundSpells.append(nowSpells)
        continueSpells = list(nextRoundSpells)
        i += 1

    print "best go:"
    print "  best cost: {}".format(mincost)
    print "  best spells: {}".format(mincostspells)
    player, boss = load_stats()
    player['spells'] = intlist_to_spelllist(mincostspells, verbose=True)
    w = wins_battle(player, boss, verbose=True)
    return mincost, mincostspells


def q_1():
    mincost, mincostspells = f(prtrds=True, prtSubrds=False, verbose=False)
    return mincost


def q_2():
    mincost, mincostspells = f(
        prtrds=True, prtSubrds=False, verbose=False, bleeds=True
    )
    return mincost


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    print "#### day 22 ########################################################"
    print "\tquestion 1 answer: {}".format(q_1())
    print "\tquestion 2 answer: {}".format(q_2())
