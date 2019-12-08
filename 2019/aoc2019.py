import logging
import logging.config
import os

import yaml


with open('../logging.yaml') as fp:
    logging_config = yaml.load(fp, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)

LOGGER = logging.getLogger('day07')
LOGGER.setLevel(logging.WARN)
logging.getLogger('parso').setLevel(logging.ERROR)

POSITION = 0
IMMEDIATE = 1

def parse_opcode(x):
    return (x % 100,
            x // 100 % 10,
            x // 1_000 % 10,
            x // 1_0000 % 10)


def load_instruction(intcode, inst_ptr):
    LOGGER.debug(f'intcode[inst_ptr: inst_ptr + 4] = {intcode[inst_ptr: inst_ptr + 4]}')
    opcode = intcode[inst_ptr]

    abc = []
    for i in range(1, 4):
        try:
            abc.append(intcode[inst_ptr + i])
        except IndexError:
            abc.append(None)
    return opcode, abc


def smart_lookup(intcode, i, mode_i):
    try:
        return i if mode_i == IMMEDIATE else intcode[i]
    except (IndexError, TypeError):
        return None


def compute_intcode(intcode, inp=1):
    inst_ptr = 0
    outputs = []
    while True:
        LOGGER.info('applying instruction')
        LOGGER.debug(f'intcode = {intcode}')
        LOGGER.debug(f'inst_ptr = {inst_ptr}')

        opcode, [a, b, c] = load_instruction(intcode, inst_ptr)
        opcode, mode_a, mode_b, mode_c = parse_opcode(opcode)
        mode_a_str = 'POSITION' if mode_a == POSITION else 'IMMEDIATE'
        mode_b_str = 'POSITION' if mode_b == POSITION else 'IMMEDIATE'
        mode_c_str = 'POSITION' if mode_c == POSITION else 'IMMEDIATE'
        a_val = smart_lookup(intcode, a, mode_a)
        b_val = smart_lookup(intcode, b, mode_b)
        c_val = smart_lookup(intcode, c, mode_c)

        LOGGER.debug(f'opcode = {opcode}')
        LOGGER.debug(f'a = {a}')
        LOGGER.debug(f'mode_a = {mode_a}')
        LOGGER.debug(f'mode_a_str = {mode_a_str}')
        LOGGER.debug(f'b = {b}')
        LOGGER.debug(f'mode_b = {mode_b}')
        LOGGER.debug(f'mode_b_str = {mode_b_str}')
        LOGGER.debug(f'c = {c}')
        LOGGER.debug(f'mode_c = {mode_c}')
        LOGGER.debug(f'mode_c_str = {mode_c_str}')

        if opcode == 1:
            LOGGER.debug(f'add: {mode_a_str} {a} + {mode_b_str} {b}')
            LOGGER.debug(f'add: {a_val} + {b_val}')
            LOGGER.debug(f'save in position {c}')
            intcode[c] = a_val + b_val
            inst_ptr += 4
        elif opcode == 2:
            LOGGER.debug(f'mult: {mode_a_str} {a} * {mode_b_str} {b}')
            LOGGER.debug(f'mult: {a_val} * {b_val}')
            LOGGER.debug(f'save in position {c}')
            intcode[c] = a_val * b_val
            inst_ptr += 4
        elif opcode == 3:
            LOGGER.debug(f'read input')
            LOGGER.debug(f'save in position {a}')
            intcode[a] = inp
            inst_ptr += 2
        elif opcode == 4:
            LOGGER.debug('output')
            outputs.append(a_val)
            yield a_val
            inst_ptr += 2
        elif opcode == 5:
            LOGGER.debug('jump-if-true (aka non-zero)')
            LOGGER.debug(f'jump: {mode_a_str} {a} != 0')
            LOGGER.debug(f'jump: {a_val} != 0')
            if a_val != 0:
                inst_ptr = b_val
            else:
                inst_ptr += 3
        elif opcode == 6:
            LOGGER.debug('jump-if-false (aka zero)')
            LOGGER.debug(f'jump: {mode_a_str} {a} == 0')
            LOGGER.debug(f'jump: {a_val} == 0')
            if a_val == 0:
                inst_ptr = b_val
            else:
                inst_ptr += 3
        elif opcode == 7:
            LOGGER.debug(f'less than: {mode_a_str} {a} < {mode_b_str} {b}')
            LOGGER.debug(f'less than: {a_val} < {b_val}')
            LOGGER.debug(f'save in position {c}')
            intcode[c] = int(a_val < b_val)
            inst_ptr += 4
        elif opcode == 8:
            LOGGER.debug(f'equal: {mode_a_str} {a} == {mode_b_str} {b}')
            LOGGER.debug(f'equal: {a_val} == {b_val}')
            LOGGER.debug(f'save in position {c}')
            intcode[c] = int(a_val == b_val)
            inst_ptr += 4
        elif opcode == 99:
            return
        else:
            raise ValueError(f'opcode = {opcode}')


def test_parse_opcode():
    assert parse_opcode(1002) == (2, 0, 1, 0)


def test_compute_intcode_day_02():
    LOGGER.warning(f'day 02 tests for compute_intcode')
    tests = [([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
              [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
             ([1,0,0,0,99], [2,0,0,0,99]),
             ([2,3,0,3,99], [2,3,0,6,99]),
             ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
             ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]), ]
    for (initial_state, final_state) in tests:
        LOGGER.info(f'initial_state = {initial_state}')
        LOGGER.debug(f'final_state = {final_state}')
        for output in compute_intcode(initial_state):
            print(f'output: {output}')
        assert initial_state == final_state


def test_compute_intcode_day_05():
    LOGGER.warning(f'day 05 tests for compute_intcode')
    for inp in [1, 10, 100, 1000]:
        LOGGER.info(f'day 5 input test: {inp}') 
        for output in compute_intcode([3, 0, 4, 0, 99], inp=inp):
            assert output == inp

    def q_2(intcode, inp):
        for return_code in compute_intcode(intcode, inp):
            return return_code

    # input == 8?
    assert q_2([3,9,8,9,10,9,4,9,99,-1,8], 1) == 0
    assert q_2([3,9,8,9,10,9,4,9,99,-1,8], 8) == 1

    # input < 8?
    assert q_2([3,9,7,9,10,9,4,9,99,-1,8], 8) == 0
    assert q_2([3,9,7,9,10,9,4,9,99,-1,8], 7) == 1

    # input == 8?
    assert q_2([3,3,1108,-1,8,3,4,3,99], 1) == 0
    assert q_2([3,3,1108,-1,8,3,4,3,99], 8) == 1

    # input < 8?
    assert q_2([3,3,1107,-1,8,3,4,3,99], 8) == 0
    assert q_2([3,3,1107,-1,8,3,4,3,99], 7) == 1

    # 0 if 0, 1 else?
    assert q_2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0) == 0
    assert q_2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 8) == 1
    assert q_2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0) == 0
    assert q_2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 8) == 1

    big_prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    assert q_2(big_prog, 7) == 999
    assert q_2(big_prog, 8) == 1000
    assert q_2(big_prog, 9) == 1001


def run_tests():
    LOGGER.setLevel(logging.DEBUG)
    test_parse_opcode()
    test_compute_intcode_day_02()
    test_compute_intcode_day_05()
    LOGGER.setLevel(logging.WARN)


if __name__ == "__main__":
    run_tests()