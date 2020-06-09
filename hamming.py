from random import randint

def get_blocks(text: str):
    code = []
    for char in text:
        char = format(ord(char), 'b')
        if len(char) % 8 != 0:
            char = ('0' * (8 - len(char) % 8)) + char
        for bit in char:
            code.append(int(bit))
    return [code[i-4:i] for i in range(4, len(code) + 1, 4)]


def encode_blocks(blocks: list):
    encoded = []
    for block in blocks:
        block = block.copy()
        block.append(block[0] ^ block[1] ^ block[2])
        block.append(block[1] ^ block[2] ^ block[3])
        block.append(block[0] ^ block[1] ^ block[3])
        encoded.append(block)
    return encoded


def corrupt_blocks(blocks: list):
    corrupted = []
    for block in blocks:
        block = block.copy()
        i = randint(0, 6)
        block[i] = int(not block[i])
        corrupted.append(block)
    return corrupted


def decode_blocks(blocks: list) -> list:
    decoded = []
    for block in blocks:
        block = block.copy()
        s1 = block[4] ^ block[0] ^ block[1] ^ block[2]
        s2 = block[5] ^ block[1] ^ block[2] ^ block[3]
        s3 = block[6] ^ block[0] ^ block[1] ^ block[3]
        s = (s1, s2, s3)
        if s == (0, 0, 1):
            block[6] = int(not block[6])
        elif s == (0, 1, 0):
            block[5] = int(not block[5])
        elif s == (0, 1, 1):
            block[3] = int(not block[3])
        elif s == (1, 0, 0):
            block[4] = int(not block[4])
        elif s == (1, 0, 1):
            block[0] = int(not block[0])
        elif s == (1, 1, 0):
            block[2] = int(not block[2])
        elif s == (1, 1, 1):
            block[1] = int(not block[1])
        decoded.append(block[:4])
    return decoded


def get_text(blocks: list) -> str:
    code = ''
    for block in blocks:
        for bit in block:
            code += str(bit)
    code = [code[i-8:i] for i in range(8, len(code) + 1, 8)]
    text = ''.join([chr(int(char, 2)) for char in code])
    return text


def main():
    while True:
        blocks = get_blocks(input('Enter your text: '))
        print('Initial:', blocks)
        blocks = encode_blocks(blocks)
        print('Encoded:', blocks)
        blocks = corrupt_blocks(blocks)
        print('Corrupted:', blocks)
        blocks = decode_blocks(blocks)
        print('Decoded:', blocks)
        print('Text:', get_text(blocks))


main()