import math

rotation_constants = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                      5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

additional_constants = [int(abs(math.sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]


def pad_message(message):
    message_length_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)

    while len(message) % 64 != 56:
        message.append(0)

    message += message_length_bits.to_bytes(8, byteorder='little')
    return message


initial_buffer = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]


def rotate_left(x, amount):
    x &= 0xFFFFFFFF
    return (x << amount | x >> (32 - amount)) & 0xFFFFFFFF


def process_message(message):
    current_buffer = initial_buffer[:]

    for offset in range(0, len(message), 64):
        a, b, c, d = current_buffer
        block = message[offset: offset + 64]

        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            to_rotate = a + f + additional_constants[i] + int.from_bytes(block[4 * g: 4 * g + 4], byteorder='little')
            new_B = (b + rotate_left(to_rotate, rotation_constants[i])) & 0xFFFFFFFF

            a, b, c, d = d, new_B, b, c

        for i, value in enumerate([a, b, c, d]):
            current_buffer[i] += value
            current_buffer[i] &= 0xFFFFFFFF

    return sum(buffer_content << (32 * i) for i, buffer_content in enumerate(current_buffer))


def md_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))


def md5(msg):
    msg = bytearray(msg, 'ascii')
    msg = pad_message(msg)
    processed_msg = process_message(msg)
    message_hash = md_to_hex(processed_msg)
    return message_hash


if __name__ == "__main__":
    print(md5("steads"))
