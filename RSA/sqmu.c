#include <stdio.h>
#include <stdlib.h>
// Organização para fica mais fácil mudar para o GMP
typedef long long int operand_t;

operand_t sqmu(operand_t X, operand_t k, operand_t N);

int main() {
    operand_t a,b,n,r;
    scanf("%lld %lld %lld", &a, &b, &n);
    r = sqmu(a,b,n);
    printf("%lld\n", r);
}

operand_t sqmu(operand_t X, operand_t k, operand_t N) {
    operand_t Y = 1;
    operand_t qtdShifts = 1;
    operand_t bitAtual = 0;
    operand_t aux = k;
    // Encontrar "quantos zeros a direita" tem o MSB de k
    while (aux > 0) {
        aux = aux >> 1;
        qtdShifts++;
    }
    bitAtual = 1 << (qtdShifts - 1);
    for (int i = 0; i < qtdShifts; i++) {
        // Realiza o quadrado de Y
        Y = (Y * Y) % N;
        // Se o bit atual for 1, Realiza também a multiplicação por X
        if (k & bitAtual) {
            Y = (Y * X) % N;
        }
        // Deslocar o bit atual para a direita
        bitAtual = bitAtual >> 1;
    }
    return Y;    
}