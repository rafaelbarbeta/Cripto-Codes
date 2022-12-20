import AES

def main():
    myBytes = [0xaa,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    myKey = [0 for i in range(16)]
    debugAES = AES.AES(myBytes,myKey)
    ctext = debugAES.aesEncrypt()
    print(list(map(lambda a : hex(a),ctext)))
    clearText = debugAES.aesDecrypt()
    print(list(map(lambda a : hex(a),clearText)))

if __name__ == '__main__':
    main()