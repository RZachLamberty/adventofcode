import logging
import logging.config
import os
from functools import lru_cache

import yaml


with open('../logging.yaml') as fp:
    logging_config = yaml.load(fp, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)


FNAME = os.path.join('data', 'day07.txt')

LOGGER = logging.getLogger('day07')


test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def load_data(fname=FNAME):
    with open(fname) as fp:
        return fp.read()


def make_abs_dir(cwd, next_dir):
    if cwd == '/':
        return f"/{next_dir}"
    else:
        return f"{cwd}/{next_dir}"


def parse_data(data: str):
    lines = data.strip().split('\n')
    i = 1
    cwd = '/'
    tree = {'/': {'parent': None,
                  'subdirs': set(),
                  'files': {}}}

    while i < len(lines) - 1:
        line = lines[i]
        if line.startswith('$ cd'):
            *_, next_dir = line.strip().split(' ')
            if next_dir == '..':
                next_dir = tree[cwd]['parent']
            else:
                next_dir = make_abs_dir(cwd, next_dir)
                if next_dir not in tree:
                    tree[next_dir] = {'parent': cwd,
                                      'subdirs': set(),
                                      'files': {}}
            cwd = next_dir
            i += 1
        elif line.startswith('$ ls'):
            while i < len(lines) - 1:
                i += 1
                line = lines[i]
                if line.startswith('$'):
                    break
                elif line.startswith('dir'):
                    _, subdir = line.split(' ')
                    subdir = make_abs_dir(cwd, subdir)
                    tree[cwd]['subdirs'].add(subdir)
                    if subdir not in tree:
                        tree[subdir] = {'parent': cwd,
                                        'subdirs': set(),
                                        'files': {}}
                else:
                    size, filename = line.split(' ')
                    size = int(size)
                    tree[cwd]['files'][filename] = size
    return tree


def p1(data):
    tree = parse_data(data)

    @lru_cache()
    def get_dir_size(dirname):
        file_size = sum(tree[dirname]['files'].values())
        subdir_size = sum(get_dir_size(subdirname) for subdirname in tree[dirname]['subdirs'])
        return file_size + subdir_size

    dir_sizes = {k: get_dir_size(k) for k in tree.keys()}
    return sum(v for v in dir_sizes.values() if v <= 100000)


assert p1(test_data) == 95437
print(f'p1: {p1(load_data())}')


def p2(data):
    tree = parse_data(data)

    @lru_cache()
    def get_dir_size(dirname):
        file_size = sum(tree[dirname]['files'].values())
        subdir_size = sum(get_dir_size(subdirname) for subdirname in tree[dirname]['subdirs'])
        return file_size + subdir_size

    dir_sizes = {k: get_dir_size(k) for k in tree.keys()}
    disk_size = 70_000_000
    root_size = dir_sizes['/']
    unused_space = disk_size - root_size
    update_size = 30_000_000
    free_up_size = update_size - unused_space
    return min(v for v in dir_sizes.values() if v >= free_up_size)


assert p2(test_data) == 24933642
print(f'p2: {p2(load_data())}')
