def main():
    N,E,C = tuple(input().split(" "))
    N = int(N)
    E = int(E)
    C = int(C)
    # Fatoração de N. Só testa números ímpares
    p = 0
    q = 0
    for i in range(3, N,2):
        if N % i == 0:
            p = i
            q = N//i
            break
    # cálculo de phi(N)
    phi = (p-1)*(q-1)
    # cálculo de d com ajuda do algoritmo extendido de Euclides
    T1 = 0
    T2 = 1
    if E > phi:
        A = E
        B = phi
    else:
        A = phi
        B = E

    while B > 0:
        Q = A // B
        R = A % B
        T = T1 - T2 * Q
        A = B
        B = R
        T1 = T2
        T2 = T

    if (T1 < 0): 
        T1 = T1 + phi
    d = T1

    # cálculo de M
    M = pow(C, d, N)
    print(M)

if __name__ == '__main__':
    main()