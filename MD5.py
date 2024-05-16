import math
import tkinter as tk
from tkinter import ttk

rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
             5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
             6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]


def pad(msg):
    msg_len_in_bits = (8 * len(msg)) & 0xffffffffffffffff
    msg.append(0x80)

    while len(msg) % 64 != 56:
        msg.append(0)

    msg += msg_len_in_bits.to_bytes(8, byteorder='little')

    return msg


init_MDBuffer = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]


# UTILITY/HELPER FUNCTION:
def leftRotate(x, amount):
    x &= 0xFFFFFFFF
    return (x << amount | x >> (32 - amount)) & 0xFFFFFFFF


block_i = 0
iteration_j = 0

labels = []


def change_block():
    global block_i
    global iteration_j

    if len(data) - 1 > block_i:
        block_i += 1
        iteration_j = 0
        labels[12].configure(text='F1')
    else:
        return

    labels[0].configure(text=data[block_i][block_i][0].hex())

    labels[3].configure(text=str(hex(data[block_i][0][1][iteration_j][0])).replace('0x', ''))
    labels[4].configure(text=str(hex(data[block_i][0][1][iteration_j][1])).replace('0x', ''))
    labels[5].configure(text=str(hex(data[block_i][0][1][iteration_j][2])).replace('0x', ''))
    labels[6].configure(text=str(hex(data[block_i][0][1][iteration_j][3])).replace('0x', ''))

    labels[7].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][0])).replace('0x', ''))
    labels[8].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][1])).replace('0x', ''))
    labels[9].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][2])).replace('0x', ''))
    labels[10].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][3])).replace('0x', ''))

    labels[1].configure(text=constants[iteration_j])
    labels[11].configure(text=f'<<<{rotate_by[iteration_j]}')

    labels[13].configure(text=f'Блок: {block_i + 1}')
    labels[14].configure(text=f'Раунд: {1}')
    labels[15].configure(text=f'Итерация: {iteration_j + 1}')


def change_round():
    global block_i
    global iteration_j

    if iteration_j < 16:
        labels[12].configure(text='F2')
        labels[14].configure(text=f'Раунд: {2}')
        iteration_j = 16
    elif 16 <= iteration_j < 32:
        labels[12].configure(text='F3')
        labels[14].configure(text=f'Раунд: {3}')
        iteration_j = 32
    elif 32 <= iteration_j < 48:
        labels[12].configure(text='F4')
        labels[14].configure(text=f'Раунд: {4}')
        iteration_j = 48
    elif 48 <= iteration_j < 64:
        if len(data) - 1 > block_i:
            block_i += 1
            iteration_j = 0
            labels[12].configure(text='F1')
            labels[14].configure(text=f'Раунд: {1}')
        else:
            return
    elif iteration_j == 64:
        if len(data) - 1 > block_i:
            block_i += 1
            iteration_j = 0
            labels[12].configure(text='F1')
            labels[14].configure(text=f'Раунд: {1}')
        else:
            return

    labels[0].configure(text=data[block_i][block_i][0].hex())

    labels[3].configure(text=str(hex(data[block_i][0][1][iteration_j][0])).replace('0x', ''))
    labels[4].configure(text=str(hex(data[block_i][0][1][iteration_j][1])).replace('0x', ''))
    labels[5].configure(text=str(hex(data[block_i][0][1][iteration_j][2])).replace('0x', ''))
    labels[6].configure(text=str(hex(data[block_i][0][1][iteration_j][3])).replace('0x', ''))

    labels[7].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][0])).replace('0x', ''))
    labels[8].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][1])).replace('0x', ''))
    labels[9].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][2])).replace('0x', ''))
    labels[10].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][3])).replace('0x', ''))

    labels[1].configure(text=constants[iteration_j])
    labels[11].configure(text=f'<<<{rotate_by[iteration_j]}')

    labels[13].configure(text=f'Блок: {block_i + 1}')
    labels[15].configure(text=f'Итерация: {iteration_j}')


def change_iteration():
    global block_i
    global iteration_j

    if iteration_j == 64:
        return

    labels[0].configure(text=data[block_i][block_i][0].hex())

    labels[3].configure(text=str(hex(data[block_i][0][1][iteration_j][0])).replace('0x', ''))
    labels[4].configure(text=str(hex(data[block_i][0][1][iteration_j][1])).replace('0x', ''))
    labels[5].configure(text=str(hex(data[block_i][0][1][iteration_j][2])).replace('0x', ''))
    labels[6].configure(text=str(hex(data[block_i][0][1][iteration_j][3])).replace('0x', ''))

    labels[7].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][0])).replace('0x', ''))
    labels[8].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][1])).replace('0x', ''))
    labels[9].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][2])).replace('0x', ''))
    labels[10].configure(text=str(hex(data[block_i][0][1][iteration_j + 1][3])).replace('0x', ''))

    labels[1].configure(text=constants[iteration_j])
    labels[11].configure(text=f'<<<{rotate_by[iteration_j]}')

    if iteration_j < 16:
        labels[12].configure(text='F1')
        labels[14].configure(text=f'Раунд: {1}')
    elif 16 <= iteration_j < 32:
        labels[12].configure(text='F2')
        labels[14].configure(text=f'Раунд: {2}')
    elif 32 <= iteration_j < 48:
        labels[12].configure(text='F3')
        labels[14].configure(text=f'Раунд: {3}')
    elif 48 <= iteration_j < 65:
        labels[12].configure(text='F4')
        labels[14].configure(text=f'Раунд: {4}')

    if iteration_j == 64:
        if len(data) - 1 > block_i:
            print('awdadsdawd')
            block_i += 1
            iteration_j = 0
        else:
            return
    else:
        iteration_j += 1

    labels[13].configure(text=f'Блок: {block_i + 1}')
    labels[15].configure(text=f'Итерация: {iteration_j}')


data = []


def processMessage(msg, labels):
    global data

    init_temp = init_MDBuffer[:]

    blocks = []

    for offset in range(0, len(msg), 64):

        A, B, C, D = init_temp  # have to initialise MD Buffer for every block

        block = msg[offset: offset + 64]  # create block to be processed

        iterations = [[A, B, C, D]]

        for i in range(64):
            if i < 16:
                func = lambda b, c, d: (b & c) | (~b & d)
                index_func = lambda i: i

            elif 16 <= i < 32:
                func = lambda b, c, d: (d & b) | (~d & c)
                index_func = lambda i: (5 * i + 1) % 16

            elif 32 <= i < 48:
                func = lambda b, c, d: b ^ c ^ d
                index_func = lambda i: (3 * i + 5) % 16

            elif 48 <= i < 64:
                func = lambda b, c, d: c ^ (b | ~d)
                index_func = lambda i: (7 * i) % 16

            F = func(B, C, D)
            G = index_func(i)

            to_rotate = A + F + constants[i] + int.from_bytes(block[4 * G: 4 * G + 4], byteorder='little')
            newB = (B + leftRotate(to_rotate, rotate_by[i])) & 0xFFFFFFFF

            A, B, C, D = D, newB, B, C

            iterations.append([A, B, C, D])

        blocks.append([block, iterations, offset])
        data.append(blocks)

        for i, val in enumerate([A, B, C, D]):
            init_temp[i] += val
            init_temp[i] &= 0xFFFFFFFF

    return sum(buffer_content << (32 * i) for i, buffer_content in enumerate(init_temp))


def MD_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))


def md5(msg, _labels, buttons, output: ttk.Entry, entry_text: tk.StringVar):
    global labels
    labels = _labels

    global data
    data.clear()

    global block_i
    global iteration_j
    block_i = 0
    iteration_j = 1

    msg = bytearray(msg, 'utf-8')
    msg = pad(msg)

    _labels[2].configure(text=msg.hex())

    processed_msg = processMessage(msg, labels)

    buttons[0].configure(command=change_block)
    buttons[1].configure(command=change_round)
    buttons[2].configure(command=change_iteration)

    labels[0].configure(text=data[0][0][0].hex())

    labels[3].configure(text=str(hex(data[0][0][1][0][0])).replace('0x', ''))
    labels[4].configure(text=str(hex(data[0][0][1][0][1])).replace('0x', ''))
    labels[5].configure(text=str(hex(data[0][0][1][0][2])).replace('0x', ''))
    labels[6].configure(text=str(hex(data[0][0][1][0][3])).replace('0x', ''))

    labels[7].configure(text=str(hex(data[0][0][1][0 + 1][0])).replace('0x', ''))
    labels[8].configure(text=str(hex(data[0][0][1][0 + 1][1])).replace('0x', ''))
    labels[9].configure(text=str(hex(data[0][0][1][0 + 1][2])).replace('0x', ''))
    labels[10].configure(text=str(hex(data[0][0][1][0 + 1][3])).replace('0x', ''))

    labels[1].configure(text=constants[0])
    labels[11].configure(text=f'<<<{rotate_by[0]}')

    labels[12].configure(text='F1')
    labels[13].configure(text=f'Блок: {0 + 1}')
    labels[14].configure(text=f'Раунд: {1}')
    labels[15].configure(text=f'Итерация: {0 + 1}')

    entry_text = entry_text.set(MD_to_hex(processed_msg))
    output.configure(textvariable=entry_text)


if __name__ == '__main__':
    message = input()
    md5(message)
