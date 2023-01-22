#include <stdio.h>
#include <stdlib.h>
// Organização para fica mais fácil mudar para o GMP
typedef long long int operand_t;

operand_t inversoModular(operand_t a, operand_t b);
operand_t gcd(operand_t a, operand_t b);

int main() {
    operand_t a,b,gcd_n,inverso;
    scanf("%lld %lld", &a, &b);
    gcd_n = gcd(a,b);
    inverso = inversoModular(a,b);
    // gcd(a,b) == 1 então a e b são primos entre si (inverso modular existe)
    if (gcd_n == 1) {
        printf("%lld %lld\n", gcd_n, inverso);
    }
    else {
        printf("%lld N\n", gcd_n);
    }
}

// a é o número que queremos o inverso modular, e b é o módulo
operand_t inversoModular(operand_t a, operand_t b) {
    operand_t A, B, T1 = 0, T2 = 1;
    operand_t Q, R, T;
    if (a > b) {
        A = a;
        B = b;
    }
    else {
        A = b;
        B = a;
    }
    // Algoritmo de Euclides Extendido
    while (B > 0) {
        Q = A / B;
        R = A % B;
        T = T1 - T2 * Q;
        A = B;
        B = R;
        T1 = T2;
        T2 = T;
    }

    if (A == 1) {
        // O inverso modular deve ser um valor positivo
        if (T1 < 0) {
            T1 = T1 + b;
        }
        return T1;
    }
    else {
        return -1;
    }
}

operand_t gcd(operand_t a, operand_t b) {
    operand_t A = a, B = b, R;
    while (B > 0) {
        R = A % B;
        A = B;
        B = R;
    }
    return A;
}