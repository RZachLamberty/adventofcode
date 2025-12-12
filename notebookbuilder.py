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
import datetime
import logging
import logging.config
import os

import yaml
from yaml import SafeLoader

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))

FTEMPLATE = os.path.join(HERE, 'aoc_template.ipynb')

LOGGER = logging.getLogger()
LOGCONF = os.path.join(HERE, 'logging.yaml')
with open(LOGCONF, 'rb') as f:
    logging.config.dictConfig(yaml.load(f, SafeLoader))


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def _target_files(year=2018, rootdir=HERE):
    """generate file paths"""
    for i in range(1, 26):
        yield i, os.path.join(rootdir, str(year), f'day{i:0>2}.ipynb')


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
    d = os.path.join(rootdir, str(year))
    os.makedirs(d, exist_ok=True)
    for i, target_file in _target_files(year, rootdir):
        LOGGER.debug(f'attempting to write {target_file}')
        if os.path.isfile(target_file):
            LOGGER.debug(f'file {target_file} already exists')
        else:
            with open(ftemplate) as fp:
                s = fp.read()
            s = s.replace('_NUMBER_', f'{i}')
            s = s.replace('_0NUMBER_', f'{i:0>2}')
            s = s.replace('_YEAR_', f'{i}')
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
    parser.add_argument("-y", "--year", help=year, default=datetime.datetime.now().year)

    rootdir = 'the root directory'
    parser.add_argument("-r", "--rootdir", help=rootdir, default=HERE)

    ftemplate = 'the file path of the template'
    parser.add_argument("-f", "--ftemplate", help=ftemplate, default=FTEMPLATE)

    args = parser.parse_args()

    LOGGER.debug(f"arguments set to {vars(args)}")

    return args


if __name__ == '__main__':
    args = parse_args()
    build(
        year=args.year,
        rootdir=args.rootdir,
        ftemplate=args.ftemplate,
    )
