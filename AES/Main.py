import AES

# Programa de teste da classe AES. Permite o usuário inserir um valor hexadecimal e criptografar ou descriptografar ele
def main():
    text = input("Por favor, insira um texto em hexadecimal (16 bytes, sem espaços):")
    key = input("Por favor, insira uma chave (16 bytes, sem espaços:")
    text = [int(text[i]+text[i+1],base=16) for i in range(0,32,2)]
    key = [int(key[i]+key[i+1],base=16) for i in range(0,32,2)]
    myText = AES.AES(text,key)
    op = input("1 Criptografar\n2 Descriptografar\n")
    if op == "1":
        print(list(map(lambda hexval : hex(hexval),myText.aesEncrypt())))
    else:
        print(list(map(lambda hexval : hex(hexval),myText.aesDecrypt())))
    
    """
    Sugestão de valores para teste:
    Chave : a020010000004000b500eedead0056aa
    Texto : 00000101030307070f0f1f1f3f3f7f7f
    Criptografado : 89daa0efb9e2b49983053d05388f3d1d

    Link para testes passo a passo : https://www.cryptool.org/en/cto/aes-step-by-step
    """
if __name__ == '__main__':
    main()