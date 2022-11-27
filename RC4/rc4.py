def main():
    chave = input("Insira a chave:\n")
    texto = input("Insira o texto para criptografar/descriptografar:\n")
    textoFormatado = list(map(lambda hextexto : int(hextexto,base=16),texto.split(" ")))
    # Inicialização e permutação do vetor S
    S = [i for i in range(256)]
    T = [ord(chave[j % len(chave)]) for j in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    # Geração de fluxo
    i = 0
    j = 0
    C = list()
    for k in range(len(textoFormatado)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256 
        C.append(textoFormatado[k] ^ S[t])
    
    # impressão do resultado:
    print("ASCII:")
    for k in range(len(C)):
        print(chr(C[k]),end="")
    print()

    print("Hexadecimal:")
    for k in range(len(C)):
        print(hex(C[k]),end=" ")
    print()
    
if __name__ == '__main__':
    main()