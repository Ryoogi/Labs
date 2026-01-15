import os
os.system('cls' if os.name == 'nt' else 'clear')

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

    print(matrix)

chacha20_init_blocks(b"12345678901234567890123456789012", 1, b"123456789012")

# quarter
