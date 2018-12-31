#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: notebookbuilder.py
Author: zlamberty
Created: 2018-12-22

Description:


Usage:
    <usage>

"""

import argparse
import logging
import logging.config
import os

import yaml


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))

FTEMPLATE = os.path.join(HERE, 'aoc_template.ipynb')

LOGGER = logging.getLogger()
LOGCONF = os.path.join(HERE, 'logging.yaml')
with open(LOGCONF, 'rb') as f:
    logging.config.dictConfig(yaml.load(f))


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def _target_files(year=2018, rootdir=HERE):
    """generate file paths"""
    for i in range(1, 26):
        yield i, os.path.join(HERE, str(year), 'day{:0>2}.ipynb'.format(i))


def build(year=2018, rootdir=HERE, ftemplate=FTEMPLATE):
    """use the neighboring template file to create a family of notebooks for
    each day in the 25 advent of code days. put them all in a sub-folder based
    on the year

    args:
        year (int): year of aoc
        ftemplate (str): path to a template file

    returns:
        None

    raises:
        None

    """
    for i, target_file in _target_files(year, rootdir):
        LOGGER.debug('attempting to write {}'.format(target_file))
        if os.path.isfile(target_file):
            LOGGER.debug('file {} already exists'.format(target_file))
        else:
            with open(ftemplate) as fp:
                s = fp.read()
            s = s.replace('_NUMBER_', '{}'.format(i))
            s = s.replace('_0NUMBER_', '{:0>2}'.format(i))
            s = s.replace('_YEAR_', '{}'.format(year))
            with open(target_file, 'w') as fp:
                fp.write(s)
            LOGGER.debug('success')


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    """ Take a log file from the commmand line """
    parser = argparse.ArgumentParser()

    year = 'the year of the competition'
    parser.add_argument("-y", "--year", help=year, default=2018)

    rootdir = 'the root directory'
    parser.add_argument("-r", "--rootdir", help=rootdir, default=HERE)

    ftemplate = 'the file path of the template'
    parser.add_argument("-f", "--ftemplate", help=ftemplate, default=FTEMPLATE)

    args = parser.parse_args()

    LOGGER.debug("arguments set to {}".format(vars(args)))

    return args


if __name__ == '__main__':
    args = parse_args()
    build(
        year=args.year,
        rootdir=args.rootdir,
        ftemplate=args.ftemplate,
    )
