import functools
import itertools
import logging
import logging.config
import pprint
import os

import numpy as np
import yaml

from IPython.core.display import display
from ipywidgets import Output


with open('../logging.yaml') as fp:
    logging_config = yaml.load(fp, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)

LOGGER = logging.getLogger('aoc2019')
LOGGER.setLevel(logging.WARN)
logging.getLogger('parso').setLevel(logging.ERROR)

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADD_RELATIVE_BASE = 9
HALT = 99

READ = 0
WRITE = 1

OPS = {ADD: (READ, READ, WRITE),
       MUL: (READ, READ, WRITE),
       IN: (WRITE,),
       OUT: (READ,),
       JUMP_TRUE: (READ, READ),
       JUMP_FALSE: (READ, READ),
       LESS_THAN: (READ, READ, WRITE),
       EQUALS: (READ, READ, WRITE),
       ADD_RELATIVE_BASE: (READ,),
       HALT: (), }
INST_PTR_DELTAS = {k: len(v) + 1 for (k, v) in OPS.items()}

MODE_STR = {POSITION: 'POSITION',
            IMMEDIATE: 'IMMEDIATE',
            RELATIVE: 'RELATIVE', }


def load_intcode(f):
    with open(f) as fp:
        return [int(_) for _ in fp.read().strip().split(',')]


@functools.lru_cache(None)
def parse_opcode(x):
    return (x % 100,
            x // 100 % 10,
            x // 1_000 % 10,
            x // 1_0000 % 10)


def smart_lookup(intcode, i, mode_i, relative_base=0):
    if mode_i == IMMEDIATE:
        return i
    elif mode_i in [POSITION, RELATIVE]:
        lookup_addr = i
        if mode_i == RELATIVE:
            lookup_addr += relative_base
        if lookup_addr < 0:
            LOGGER.debug('invalid negative memory address')
            return None
        return intcode.get(lookup_addr, 0)


class IntcodeComputer:
    def __init__(self, intcode, inputs=None, inst_ptr=0, relative_base=0):
        self._orig_intcode = list(intcode)
        self._intcode = dict(enumerate(self._orig_intcode))
        self.inputs = [] if inputs is None else inputs
        #LOGGER.error(f'inputs = {inputs[:10]}')
        self.inst_ptr = inst_ptr
        self._iter = None
        self.relative_base = relative_base

    @property
    def intcode(self):
        x = [0] * (max(self._intcode.keys()) + 1)
        for (i, val) in self._intcode.items():
            x[i] = val
        return x

    def get_input(self):
        LOGGER.debug('popping from self.inputs')
        LOGGER.debug(f'inputs before: {self.inputs}')
        inp = self.inputs.pop(0)
        LOGGER.debug(f'input to load: {inp}')
        LOGGER.debug(f'inputs after: {self.inputs}')
        return inp

    def get_output(self):
        if self._iter is None:
            self._iter = self.__iter__()
        return next(self._iter)

    def load_instruction(self):
        LOGGER.debug('getting opcode and mode values')
        opcode = self._intcode[self.inst_ptr]
        opcode, mode_a, mode_b, mode_c = parse_opcode(opcode)
        modes = [mode_a, mode_b, mode_c]
        LOGGER.debug(f'intcode[ip] = {opcode}')
        LOGGER.debug(f"mode_a is {MODE_STR[mode_a]} ({mode_a})")
        LOGGER.debug(f"mode_b is {MODE_STR[mode_b]} ({mode_b})")
        LOGGER.debug(f"mode_c is {MODE_STR[mode_c]} ({mode_c})")

        LOGGER.debug('reading parameters')
        param_kinds = OPS[opcode]
        ret_list = [None] * 3
        for (i, (param_kind, mode)) in enumerate(zip(param_kinds, modes)):
            val_now = self._intcode.get(self.inst_ptr + i + 1, 0)
            LOGGER.debug(f"intcode[ip + {i + 1}] = {val_now}")
            LOGGER.debug(f"mode:{i} is {MODE_STR[mode_a]} ({mode_a})")
            if mode == IMMEDIATE:
                if param_kind == WRITE:
                    raise ValueError('wtf shouldn\'t be possible')
                LOGGER.debug('READ IMMEDIATE')
                LOGGER.debug(f'param:{i} = {val_now}')
                ret_list[i] = val_now
            elif mode in [POSITION, RELATIVE]:
                if mode == RELATIVE:
                    val_now += self.relative_base
                    LOGGER.debug(f'mode is relative, val_now = {val_now}')

                if val_now < 0:
                    msg = 'invalid negative memory address'
                    LOGGER.critical(msg)
                    raise ValueError(msg)

                if param_kind == READ:
                    new_val = self._intcode.get(val_now, 0)
                    LOGGER.debug(f'intcode[{val_now}] = {new_val}')
                    val_now = new_val
                # if write, just use the value as the register

                LOGGER.debug(f'param:{i} = {val_now}')
                ret_list[i] = val_now
            else:
                raise ValueError(f"invalid mode {mode}")

        LOGGER.debug(f'intcode[inst_ptr: inst_ptr + 4] = {ret_list}')
        inst_ptr_delta = INST_PTR_DELTAS[opcode]
        LOGGER.debug(f'moving inst_ptr forward {inst_ptr_delta} spots')
        LOGGER.debug(f'{self.inst_ptr} --> {self.inst_ptr} + {inst_ptr_delta}')
        self.inst_ptr += inst_ptr_delta
        LOGGER.debug(f'inst_ptr = {self.inst_ptr}')
        return [opcode] + ret_list

    def __iter__(self):
        while True:
            LOGGER.info('applying instruction')
            LOGGER.debug(f'intcode = {self.intcode}')
            LOGGER.debug(f'inst_ptr = {self.inst_ptr}')

            opcode, a, b, c = self.load_instruction()
            LOGGER.debug(f'opcode = {opcode}')
            LOGGER.debug(f'a = {a}')
            LOGGER.debug(f'b = {b}')
            LOGGER.debug(f'c = {c}')

            if opcode == ADD:
                LOGGER.debug(f'ADD: intcode[{c}] = {a} + {b}')
                self._intcode[c] = a + b
            elif opcode == MUL:
                LOGGER.debug(f'MUL: intcode[{c}] = {a} * {b}')
                self._intcode[c] = a * b
            elif opcode == IN:
                self._intcode[a] = self.get_input()
            elif opcode == OUT:
                LOGGER.debug(f'output {a}')
                yield a
            elif opcode == JUMP_TRUE:
                LOGGER.debug('jump-if-true (aka non-zero)')
                LOGGER.debug(f'if {a} != 0: inst_ptr = {b}')
                if a != 0:
                    self.inst_ptr = b
            elif opcode == JUMP_FALSE:
                LOGGER.debug('jump-if-false (aka zero)')
                LOGGER.debug(f'if {a} == 0: inst_ptr = {b}')
                if a == 0:
                    self.inst_ptr = b
            elif opcode == LESS_THAN:
                LOGGER.debug('less than')
                LOGGER.debug(f'intcode[c] = {a} < {b}')
                self._intcode[c] = int(a < b)
            elif opcode == EQUALS:
                LOGGER.debug('equals}')
                LOGGER.debug(f'intcode[c] = {a} == {b}')
                self._intcode[c] = int(a == b)
            elif opcode == ADD_RELATIVE_BASE:
                LOGGER.debug('updating relative base')
                LOGGER.debug(f'relative_base = {self.relative_base} + {a}')
                self.relative_base += a
            elif opcode == HALT:
                return
            else:
                raise ValueError(f'opcode = {opcode}')


# game enums
UNKNOWN = -1
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

DRAW_CHAR = {EMPTY: ' ',
             WALL: '+',
             BLOCK: '■',
             PADDLE: '─',
             BALL: '@',
             UNKNOWN: '?', }

LEFT, NEUTRAL, RIGHT = -1, 0, 1

class ArcadeGame(IntcodeComputer):
    def __init__(self, *args, **kwargs):
        """just create an output widget and otherwise defer"""
        self.screen = {}
        self.score = None
        self.out = Output(layout={'min_height': '500px'})
        self.displayed_yet = False
        super().__init__(*args, **kwargs)

    def play(self, do_draw=False):
        while True:
            try:
                self.step()
                if do_draw:
                    self.draw()
            except StopIteration:
                break
        LOGGER.info('game over!')

    def step(self):
        a = self.get_output()
        b = self.get_output()
        c = self.get_output()
        if (a, b) == (-1, 0):
            self.score = c
            LOGGER.debug(f'score updated to {self.score}')
        else:
            self.screen[a, b] = c

    @property
    def num_bricks(self):
        return len([v for v in self.screen.values() if v == BLOCK])

    @property
    def screen_as_array(self):
        x_max = y_max = -1
        x_min = y_min = np.inf

        for (x, y) in self.screen.keys():
            x_max = max(x, x_max)
            x_min = min(x, x_min)
            y_max = max(y, y_max)
            y_min = min(y, y_min)

        # note: transposing!
        z = -1 * np.ones((y_max - y_min + 1, x_max - x_min + 1))

        for (x, y), val in self.screen.items():
            # note: transposing!
            z[y - y_min, x - x_min] = val

        return z

    @property
    def screen_as_str(self):
        return '\n'.join([''.join(DRAW_CHAR[elem] for elem in row)
                          for row in self.screen_as_array])

    def _pos(self, c):
        cs = [k for (k, v) in self.screen.items() if v == c]
        if len(cs) != 1:
            raise ValueError("too many balls")
        return cs[0]

    @property
    def ball_pos(self):
        return self._pos(BALL)

    @property
    def paddle_pos(self):
        return self._pos(PADDLE)

    def get_input(self):
        LOGGER.debug('asked for input!!')
        bx = self.ball_pos[0]
        px = self.paddle_pos[0]
        if max(bx, px) > 200:
            raise ValueError()
        if bx < px:
            return LEFT
        elif px < bx:
            return RIGHT
        else:
            return NEUTRAL

    def draw(self):
        if not self.displayed_yet:
            display(self.out)
            self.displayed_yet = True
        with self.out:
            self.out.clear_output(wait=True)
            print(f'{self.screen_as_str}\n\nscore: {self.score}')


class NetworkedIntcodeComputer:
    def __init__(self, network_packet_queue, *args, **kwargs):
        self.network_packet_queue = network_packet_queue
        super().__init__(*args, **kwargs)

    def get_input(self):
        LOGGER.debug('popping from self.inputs')
        LOGGER.debug(f'inputs before: {self.inputs}')
        try:
            inp = self.inputs.pop(0)
        except IndexError:
            if self.allow_empty_inputs:
                LOGGER.debug('empty imputs are allowed')
                inp = -1
            else:
                raise
        LOGGER.debug(f'input to load: {inp}')
        LOGGER.debug(f'inputs after: {self.inputs}')
        return inp

    def __iter__(self):
        while True:
            self.step()
    
    def step(self):
        LOGGER.info('applying instruction')
        LOGGER.debug(f'intcode = {self.intcode}')
        LOGGER.debug(f'inst_ptr = {self.inst_ptr}')

        opcode, a, b, c = self.load_instruction()
        LOGGER.debug(f'opcode = {opcode}')
        LOGGER.debug(f'a = {a}')
        LOGGER.debug(f'b = {b}')
        LOGGER.debug(f'c = {c}')

        if opcode == ADD:
            LOGGER.debug(f'ADD: intcode[{c}] = {a} + {b}')
            self._intcode[c] = a + b
        elif opcode == MUL:
            LOGGER.debug(f'MUL: intcode[{c}] = {a} * {b}')
            self._intcode[c] = a * b
        elif opcode == IN:
            self._intcode[a] = self.get_input()
        elif opcode == OUT:
            LOGGER.debug(f'output {a}')
            # TODO: fix this maybe?
            yield a
        elif opcode == JUMP_TRUE:
            LOGGER.debug('jump-if-true (aka non-zero)')
            LOGGER.debug(f'if {a} != 0: inst_ptr = {b}')
            if a != 0:
                self.inst_ptr = b
        elif opcode == JUMP_FALSE:
            LOGGER.debug('jump-if-false (aka zero)')
            LOGGER.debug(f'if {a} == 0: inst_ptr = {b}')
            if a == 0:
                self.inst_ptr = b
        elif opcode == LESS_THAN:
            LOGGER.debug('less than')
            LOGGER.debug(f'intcode[c] = {a} < {b}')
            self._intcode[c] = int(a < b)
        elif opcode == EQUALS:
            LOGGER.debug('equals}')
            LOGGER.debug(f'intcode[c] = {a} == {b}')
            self._intcode[c] = int(a == b)
        elif opcode == ADD_RELATIVE_BASE:
            LOGGER.debug('updating relative base')
            LOGGER.debug(f'relative_base = {self.relative_base} + {a}')
            self.relative_base += a
        elif opcode == HALT:
            return
        else:
            raise ValueError(f'opcode = {opcode}')


class InteractiveIntcodeComputer(IntcodeComputer):
    def __init__(self, *args, command_list, security_ckpt_dir='east',
                 ultimate_inv=None, **kwargs):
        """just create an output widget and otherwise defer"""
        self.command_list = command_list if command_list is not None else []
        self.security_ckpt_dir = security_ckpt_dir
        self.ultimate_inv = ultimate_inv
        if self.ultimate_inv is None:
            self.ultimate_inv = ['pointer',
                                 'coin',
                                 'mug',
                                 'manifold',
                                 'hypercube',
                                 'easter egg',
                                 'astrolabe']
        self._currently_holding = set()
        self._too_heavy_item_sets = set()
        self._brute_force_num = 1
        self._item_set_generator = itertools.chain.from_iterable(
            itertools.combinations(l, i) for i in range(1, len(l) + 1))
        super().__init__(*args, **kwargs)
        
    def get_input(self):
        #LOGGER.warning(f'len(self.inputs) = {len(self.inputs)}')
        try:
            inp = self.inputs.pop(0)
        except IndexError:
            self.print_recents()
            
            if self.command_list:
                next_cmd = self.command_list.pop(0) + '\n'
                print(f'pre supplied command: {next_cmd}')
            elif self.doing_brute_force:
                try:
                    next_cmd = self.brute_force_command_list.pop(0) + '\n'
                    print(f'brute force command: {next_cmd}')
                except IndexError:
                    
                    self.update_brute_force_command_list()
                    next_cmd = self.brute_force_command_list.pop(0) + '\n'
                    print(f'brute force command: {next_cmd}')
            else:
                next_cmd = input() + '\n'
            
            if next_cmd == ('brute force\n'):
                print('I got u')
                self.doing_brute_force = True
                
                self.update_brute_force_command_list()
                next_cmd = self.brute_force_command_list.pop(0) + '\n'
                print(f'brute force command: {next_cmd}')
                
            self.inputs += [ord(_) for _ in next_cmd]
            inp = self.inputs.pop(0)
        return inp
    
    def update_brute_force_command_list(self):
        # basically, iterate through possible combinations of
        # items to hold, step east, and 'see if we won' (tbd)
        while True:
            try:
                next(self._item_set_generator)
        
        
        
            for item_set in itertools.combinations(self.ultimate_inv, brute_force_num):
                # is any subset of this item_set too heavy?
                is_too_heavy = any(set(item_set).intersection(sub_set) == sub_set
                                   for sub_set in too_heavy_item_sets)
                if not is_too_heavy:
                    items_to_drop = currently_holding.difference(item_set)
                    items_to_take = item_set.difference(currently_holding)
                    command_list_now = ['drop {}'.format(item) for item in items_to_drop]
                    command_list_now = ['take {}'.format(item) for item in items_to_take]
                    command_list_now += ['east']

        command_list_now = []
        for item_set in itertools.combinations(self.ultimate_inv, self._brute_force_num):
            command_list_now += ['take {}'.format(item) for item in item_set]
            command_list_now += ['east']
            command_list_now += ['drop {}'.format(item) for item in item_set]
        print('command_list_now:')
        pprint.pprint(command_list_now)
        self.command_list += command_list_now
        self._brute_force_num += 1

        next_cmd = self.command_list.pop(0) + '\n'
        
    
    def print_recents(self):
        try:
            print(''.join([chr(_) for _ in self.recent_history]))
            self.recent_history = []
        except Exception as e:
            print(e)
            print('no recent history recorded')
    
    def play(self):
        self.recent_history = []
        while True:
            self.recent_history.append(self.get_output())


def compute_intcode(intcode, inputs=[1], inst_ptr=0):
    return IntcodeComputer(intcode=intcode,
                           inputs=inputs,
                           inst_ptr=inst_ptr)


def test_parse_opcode():
    assert parse_opcode(1002) == (2, 0, 1, 0)


def test_compute_intcode_day_02():
    LOGGER.warning(f'day 02 tests for compute_intcode')
    tests = [([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
              [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
             ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
             ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
             ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
             ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]), ]
    for (initial_state, final_state) in tests:
        LOGGER.info(f'initial_state = {initial_state}')
        LOGGER.debug(f'final_state = {final_state}')
        ic = IntcodeComputer(intcode=initial_state)
        for output in ic:
            print(f'output: {output}')
        assert ic.intcode == final_state, f'initial_state = {initial_state}\nfinal_state = {final_state}'


def test_compute_intcode_day_05():
    LOGGER.warning(f'day 05 tests for compute_intcode')
    for inp in [1, 10, 100, 1000]:
        LOGGER.info(f'day 5 input test: {inp}')
        for output in compute_intcode([3, 0, 4, 0, 99], inputs=[inp]):
            assert output == inp

    def q_2(intcode, inp):
        for return_code in compute_intcode(intcode, [inp]):
            return return_code

    # input == 8?
    assert q_2([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1) == 0
    assert q_2([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8) == 1

    # input < 8?
    assert q_2([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8) == 0
    assert q_2([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7) == 1

    # input == 8?
    assert q_2([3, 3, 1108, -1, 8, 3, 4, 3, 99], 1) == 0
    assert q_2([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8) == 1

    # input < 8?
    assert q_2([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8) == 0
    assert q_2([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7) == 1

    # 0 if 0, 1 else?
    assert q_2([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
               0) == 0
    assert q_2([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
               8) == 1
    assert q_2([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0) == 0
    assert q_2([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 8) == 1

    big_prog = [
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999,
        1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    assert q_2(big_prog, 7) == 999
    assert q_2(big_prog, 8) == 1000
    assert q_2(big_prog, 9) == 1001


def test_compute_intcode_day_07():
    pass


def test_compute_intcode_day_09():
    LOGGER.warning(f'day 09 tests for compute_intcode')
    test_ic = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101,
               1006, 101, 0, 99]
    ic = IntcodeComputer(intcode=test_ic, inputs=[None])
    output = list(ic)
    assert output == test_ic

    test_ic = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    ic = IntcodeComputer(intcode=test_ic)
    output = ic.get_output()
    assert len(str(output)) == 16

    test_ic = [104, 1125899906842624, 99]
    ic = IntcodeComputer(intcode=test_ic)
    output = ic.get_output()
    assert output == test_ic[1]


def run_tests():
    LOGGER.setLevel(logging.DEBUG)
    test_parse_opcode()
    test_compute_intcode_day_02()
    test_compute_intcode_day_05()
    test_compute_intcode_day_07()
    test_compute_intcode_day_09()
    LOGGER.setLevel(logging.WARN)


if __name__ == "__main__":
    run_tests()
