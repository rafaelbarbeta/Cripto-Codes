#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>

int main() {
    int base;
    mpz_t n,exp,m;
    mpz_init(n);
    mpz_init(exp);
    mpz_init(m);
    scanf("%d", &base);
    if (base == 10) {
        gmp_scanf("%Zd", &n);
        gmp_scanf("%Zd", &exp);
        gmp_scanf("%Zd", &m);
    }
    else {
        gmp_scanf("%Zx", &n);
        gmp_scanf("%Zx", &exp);
        gmp_scanf("%Zx", &m);
    }
    // Usando o algoritmo de exponenciação quadrado e multiplicação
    mpz_t Y;
    mpz_t qtdShifts;
    mpz_t bitAtual;
    mpz_t aux;
    mpz_t X;
    mpz_init(Y);
    mpz_init(qtdShifts);
    mpz_init(bitAtual);
    mpz_init(aux);
    mpz_init(X);
    mpz_set_ui(Y, 1);
    mpz_set_ui(qtdShifts, 1);
    mpz_set_ui(bitAtual, 0);
    mpz_set(aux, exp);
    mpz_set(X, m);

    // Encontrar "quantos zeros a direita" tem o MSB de k
    while (mpz_cmp_ui(aux, 0) > 0) {
        mpz_tdiv_q_2exp(aux, aux, 1);
        mpz_add_ui(qtdShifts, qtdShifts, 1);
    }
    mpz_set_ui(bitAtual, 1);
    mpz_sub_ui(qtdShifts, qtdShifts, 1);
    mpz_mul_2exp(bitAtual, bitAtual, mpz_get_ui(qtdShifts));
    for (int i = 0; i <= mpz_get_ui(qtdShifts); i++) {
        // Realiza o quadrado de Y
        mpz_mul(Y, Y, Y);
        mpz_mod(Y, Y, n);
        // Se o bit atual for 1, Realiza também a multiplicação por X
        if (mpz_tstbit(exp, i)) {
            mpz_mul(Y, Y, X);
            mpz_mod(Y, Y, n);
        }
        // Realiza um deslocamento para a direita
        mpz_tdiv_q_2exp(bitAtual, bitAtual, 1);
        
    }
    if (base == 10) {
        printf("base = %d\n",10);
        gmp_printf("m/c = %Zd\n", Y);
    }
    else {
        printf("base = %d\n",16);
        gmp_printf("m/c = %Zx\n", Y);
    }
}