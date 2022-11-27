def crack_one_time_pad(ciphertext1, ciphertext2):
    """Crack a one-time pad given two ciphertexts."""
    return ' '.join([hex(int(c1,base=16) ^ int(c2,base=16)) for c1, c2 in zip(ciphertext1, ciphertext2)])

cp1 = input("Insert text 1:").split(" ")
cp2 = input("Insert text 2:").split(" ")
print(crack_one_time_pad(cp1, cp2))