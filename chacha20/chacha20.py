import os
os.system('cls' if os.name == 'nt' else 'clear')

def rotl(value, shift):
    return (value << shift) & 0xffffffff | value >> (32 - shift)

# chacha20_init_blocks
def chacha20_init_blocks(key: bytes, counter: int, nonce: bytes):
    print(dir(key))
    # validate
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes length!")
    if len(nonce) != 12:
        raise ValueError("Nonce must be 12 bytes length!")
    if not isinstance(counter, int):
        raise TypeError("Counter must be integer!")
    
    matrix = []
    # print(dir(counter))
    print()
    # text[start:stop:step]
    string = b"expand 32-byte k"

    for i in range (0, len(string), 4): 
        matrix.append(int.from_bytes(string[i:i+4], 'little'))

    # key
    for i in range (0, len(key), 4):
        matrix.append(int.from_bytes(key[i:i+4], 'little'))  
    # counter
    matrix.append(counter & 0xffffffff)
    # nonce
    for i in range (0, len(nonce), 4):
        matrix.append(int.from_bytes(nonce[i:i+4], 'little'))

    return matrix

# quarter_round
def quarter_round(state, a, b, c, d):
    # set 1
    state[a] = (state [a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotl(state[d], 16)
    
    state[c] = (state [c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotl(state[b], 12)

    # set 2
    state[a] = (state [a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotl(state[d], 8)
    
    state[c] = (state [c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotl(state[b], 7)

# init temp tester
init_state = chacha20_init_blocks(b"12345678901234567890123456789012", 1, b"123456789012")
working_state = init_state[:]

for i in range(10):
    # column round
    quarter_round(working_state, 0, 4, 8, 12)
    quarter_round(working_state, 1, 5, 9, 13)
    quarter_round(working_state, 2, 6, 10, 14)
    quarter_round(working_state, 3, 7, 11, 15)

    # diagonal round
    quarter_round(working_state, 0, 5, 10, 15)
    quarter_round(working_state, 1, 6, 11, 12)
    quarter_round(working_state, 2, 7, 8, 13)
    quarter_round(working_state, 3, 4, 9, 14)

final_state = [(init_state[i] + working_state[i]) & 0xffffffff for i in range (16)]

