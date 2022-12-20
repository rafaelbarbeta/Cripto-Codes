# "Adiciona" (XOR) uma subchave ao estado.
# Retorna a matriz de estado com com a chave adicionada
def addKey(state,subkey):
    result = []
    # Itera a matriz de estado e subchave e faz XOR byte a byte
    for lineState,lineSubkey in zip(state,subkey):
        result.append(list(map(lambda hex1,hex2 : hex1 ^ hex2,lineState,lineSubkey)))
    return result

# Realiza a substituição de bytes de acordo com a tabela "SBox"
def subBytes(state,Sbox):
    for i in range(4):
        for j in range(4):
            state[i][j] = Sbox[state[i][j]]

# Faz o shift das linhas da matriz de estado. Parte da Camada de Difusão
def shiftRow(state):
    # Shift 1 Segunda linha
    b1 = state[1][0]
    state[1].pop(0)
    state[1].append(b1)

    # Shift 2 Terceira linha
    b2 = state[2][0]
    b6 = state[2][1]
    state[2].pop(0)
    state[2].pop(0)
    state[2].append(b2)
    state[2].append(b6)

    # Shift 2 Terceira linha
    b3 = state[3][0]
    b7 = state[3][1]
    b11 = state[3][2]
    state[3].pop(0)
    state[3].pop(0)
    state[3].pop(0)
    state[3].append(b3)
    state[3].append(b7)
    state[3].append(b11)

# Realiza uma multiplicação dentro do corpo de Galois GF(2^8) e retorna o resultado
# A função aceita as constantes utilizadas na mistura de colunas, 1 2 e 3 "constant" e o byte "base"
def gfMultiply(base,constant):
    if constant == 1:
        return base
    # Multiplicar por 2, basta fazer 1 shift a esquerda da base
    # Se a base for maior que 0x80, então é necessário fazer um XOR com o polinônio irredutível cujo valor é 0x11b
    elif constant == 2:
        if base >= 0x80:
            res = base << 1
            res = res ^ 0x11b
        else:
            res = base << 1
        return res
    # De forma semelhante, multiplicar por 3 basta fazer o processo acima e "adicionar" (XOR) a base
    # O polinômio que ele representa é (x+1), por isso desse processo
    elif constant == 3:
        if base >= 0x80:
            res = base << 1
            res = res ^ 0x11b
            res = res ^ base
        else:
            res = base << 1
            res = res ^ base
        return res
    return None

# Realiza uma soma no corpo de Galois GF(2^8) de quatro elementos
# Recebe duas bases no valor máximo de 255 (1 byte) e retorna a soma, simplesmente um xor
def gfAdd(base1,base2,base3,base4):
    return base1 ^ base2 ^ base3 ^ base4

# Realiza a etapa de mistura de colunas utilizando como parâmetro "mixMatrix"
def mixColumns(state,mixMatrix):
    newState = [[],[],[],[]]
    for i in range(4):
        # Byte misturado da linha 1
        newbyte0 = gfAdd(
            gfMultiply(state[0][i],mixMatrix[0][0]),
            gfMultiply(state[1][i],mixMatrix[0][1]),
            gfMultiply(state[2][i],mixMatrix[0][2]),
            gfMultiply(state[3][i],mixMatrix[0][3])
        )
        # Byte misturado da linha 2
        newbyte1 = gfAdd(
            gfMultiply(state[0][i],mixMatrix[1][0]),
            gfMultiply(state[1][i],mixMatrix[1][1]),
            gfMultiply(state[2][i],mixMatrix[1][2]),
            gfMultiply(state[3][i],mixMatrix[1][3])
        )
        # Byte misturado da linha 3
        newbyte2 = gfAdd(
            gfMultiply(state[0][i],mixMatrix[2][0]),
            gfMultiply(state[1][i],mixMatrix[2][1]),
            gfMultiply(state[2][i],mixMatrix[2][2]),
            gfMultiply(state[3][i],mixMatrix[2][3])
        )
        # Byte misturado da linha 4
        newbyte3 = gfAdd(
            gfMultiply(state[0][i],mixMatrix[3][0]),
            gfMultiply(state[1][i],mixMatrix[3][1]),
            gfMultiply(state[2][i],mixMatrix[3][2]),
            gfMultiply(state[3][i],mixMatrix[3][3])
        )
        # Coloca os bytes computados na matriz 'newState'
        newState[0].append(newbyte0)
        newState[1].append(newbyte1)
        newState[2].append(newbyte2)
        newState[3].append(newbyte3)
    return newState

# Função para transformar uma lista de 16 bytes em uma matriz 4 x 4 
def matrixTransfrom(byteList):
    byteMatrix = [[],[],[],[]]
    k = 0
    for i in range(4):
      for j in range(4):
          byteMatrix[j].append(byteList[k])
          k += 1
    return byteMatrix

# Função g() da expansão de chave.
# Recebe os 32 bits 'w32bit', a S-box e o índice atual "rci" para a round constant        
def gFunc(w32bit,rci,Sbox):
    # Definição dos valores da round constant
    rcon = [0x01, 0x02,	0x04,	0x08,	0x10,	0x20,	0x40,	0x80,	0x1B,	0x36]
    # Rotação dos 4 bytes
    v0 = w32bit[0]
    w32bit.pop(0)
    w32bit.append(v0)
    
    # Substituição com o S-Box
    Sw32bit = list(map(lambda hex: Sbox[hex],w32bit))
    # XOR lógico com a constante 
    Sw32bit[0] = (rcon[rci] ^ Sw32bit[0])
    # Retorna o valor da função g, de 32 bits
    return Sw32bit

# Gera as subchaves a partir da chave principal. Retorna uma lista com as chaves
# 'key' é uma lista de 16 objetos do tipo inteiro
# retorna uma lista com todas as subchaves. 
def genSubKeys(key,SBox):
    W = list()
    subKeys = list()
    subKeys.append(key)
    # Gera uma lista de 32 bits para formar os valores de W.
    for i in range(0,len(key),4):
        W.append([key[i],key[i+1],key[i+2],key[i+3]])
    # Aplica as transformações para a geração das próximas round key
    for i in range(10):
        W[0] = list(map(lambda hex1, hex2 :hex1 ^ hex2,W[0],gFunc(list(W[3]),i,SBox)))
        W[1] = list(map(lambda hex1, hex2 :hex1 ^ hex2,W[0],W[1]))
        W[2] = list(map(lambda hex1, hex2 :hex1 ^ hex2,W[1],W[2]))
        W[3] = list(map(lambda hex1, hex2 :hex1 ^ hex2,W[2],W[3]))
        subKeys.append([byte for w32bit in W for byte in w32bit])
    return list(map(matrixTransfrom,subKeys))

# Realiza um round completo do AES. (Substituição, trocar linhas, misturar colunas)
# Recebe uma matriz de estado, uma subchave e as tabelas de embaralhamento
# O booleano "omitMix" é utilizado para desabilitar o mixColumns no último round, segundo a espec do AES
def round(state,subkey,SBox,mixMatrix,omitMix):
    for line in state:
      print(list(map(lambda hex1 : hex(hex1),line)))
    print()
    subBytes(state,SBox)
    shiftRow(state)
    if omitMix != True:
        state = mixColumns(state,mixMatrix)
    state = addKey(state,subkey)
    return state

# Função principal, criptografa um texto dado por um vetor de 16 bytes e retorna o resultado
def aesEncrypt(clearText,key):
  SBox = [
  0x63,	0x7c,	0x77,	0x7b,	0xf2,	0x6b,	0x6f,	0xc5,	0x30,	0x01,	0x67,	0x2b,	0xfe,	0xd7,	0xab,	0x76,
  0xca,	0x82,	0xc9,	0x7d,	0xfa,	0x59,	0x47,	0xf0,	0xad,	0xd4,	0xa2,	0xaf,	0x9c,	0xa4,	0x72,	0xc0,
  0xb7,	0xfd,	0x93,	0x26,	0x36,	0x3f,	0xf7,	0xcc,	0x34,	0xa5,	0xe5,	0xf1,	0x71,	0xd8,	0x31,	0x15,
  0x04,	0xc7,	0x23,	0xc3,	0x18,	0x96,	0x05,	0x9a,	0x07,	0x12,	0x80,	0xe2,	0xeb,	0x27,	0xb2,	0x75,
  0x09,	0x83,	0x2c,	0x1a,	0x1b,	0x6e,	0x5a,	0xa0,	0x52,	0x3b,	0xd6,	0xb3,	0x29,	0xe3,	0x2f,	0x84,
  0x53,	0xd1,	0x00,	0xed,	0x20,	0xfc,	0xb1,	0x5b,	0x6a,	0xcb,	0xbe,	0x39,	0x4a,	0x4c,	0x58,	0xcf,
  0xd0,	0xef,	0xaa,	0xfb,	0x43,	0x4d,	0x33,	0x85,	0x45,	0xf9,	0x02,	0x7f,	0x50,	0x3c,	0x9f,	0xa8,
  0x51,	0xa3,	0x40,	0x8f,	0x92,	0x9d,	0x38,	0xf5,	0xbc,	0xb6,	0xda,	0x21,	0x10,	0xff,	0xf3,	0xd2,
  0xcd,	0x0c,	0x13,	0xec,	0x5f,	0x97,	0x44,	0x17,	0xc4,	0xa7,	0x7e,	0x3d,	0x64,	0x5d,	0x19,	0x73,
  0x60,	0x81,	0x4f,	0xdc,	0x22,	0x2a,	0x90,	0x88,	0x46,	0xee,	0xb8,	0x14,	0xde,	0x5e,	0x0b,	0xdb,
  0xe0,	0x32,	0x3a,	0x0a,	0x49,	0x06,	0x24,	0x5c,	0xc2,	0xd3,	0xac,	0x62,	0x91,	0x95,	0xe4,	0x79,
  0xe7,	0xc8,	0x37,	0x6d,	0x8d,	0xd5,	0x4e,	0xa9,	0x6c,	0x56,	0xf4,	0xea,	0x65,	0x7a,	0xae,	0x08,
  0xba,	0x78,	0x25,	0x2e,	0x1c,	0xa6,	0xb4,	0xc6,	0xe8,	0xdd,	0x74,	0x1f,	0x4b,	0xbd,	0x8b,	0x8a,
  0x70,	0x3e,	0xb5,	0x66,	0x48,	0x03,	0xf6,	0x0e,	0x61,	0x35,	0x57,	0xb9,	0x86,	0xc1,	0x1d,	0x9e,
  0xe1,	0xf8,	0x98,	0x11,	0x69,	0xd9,	0x8e,	0x94,	0x9b,	0x1e,	0x87,	0xe9,	0xce,	0x55,	0x28,	0xdf,
  0x8c,	0xa1,	0x89,	0x0d,	0xbf,	0xe6,	0x42,	0x68,	0x41,	0x99,	0x2d,	0x0f,	0xb0,	0x54,	0xbb,	0x16,
]
  MixColumnMatrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
  ]
  subKeys = genSubKeys(key,SBox)
  state = matrixTransfrom(clearText)
  state = addKey(state,subKeys[0])
  for i in range(1,11):
    state = round(state,subKeys[i],SBox,MixColumnMatrix,i == 10)
  return state


def main():
  myBytes = [0xaa,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
  myKey = [0 for i in range(16)]
  ctext = aesEncrypt(myBytes,myKey)
  for line in ctext:
      print(list(map(lambda hex1 : hex(hex1),line)))

if __name__ == '__main__':
    main()