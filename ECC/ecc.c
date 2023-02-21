// NOME : Rafael Gimenez Barbeta RA : 804318
#include <stdio.h>
#include <stdlib.h>

typedef long long int bigint;

typedef struct {
    bigint X;
    bigint Y;
} Ponto;

bigint inversoModular(bigint a,bigint b);
bigint calcularLambda(Ponto Q, Ponto G,bigint a,bigint p);
Ponto somaPontos(Ponto Q, Ponto G,bigint a,bigint p);
Ponto multiplicarPonto(Ponto Q,bigint n,bigint a,bigint p);
int pontoIgual(Ponto Q, Ponto G);
Ponto negativoPonto(Ponto Q,bigint p);
int pontoEhZero(Ponto Q);
bigint modulo(bigint a,bigint b);
bigint addMod(bigint a, bigint b, bigint p);
bigint subMod(bigint a, bigint b, bigint p);
bigint mulMod(bigint a, bigint b, bigint p);
bigint divMod(bigint a, bigint b, bigint p);

int main() {
    bigint n,a,p;
    Ponto G,R;
    while (1) {
        scanf("%lld",&n);
        if (n == 0) {
            break;
        }
        scanf("%lld %lld %lld %lld",&a,&p,&G.X,&G.Y);
        R = multiplicarPonto(G, n, a, p);
        printf("%lld %lld\n",R.X,R.Y);
    }
    return 0;
}

// a é o número que queremos o inverso modular, e b é o módulo
bigint inversoModular(bigint a,bigint b) {
    bigint A, B, T1 = 0, T2 = 1;
    bigint Q, R, T;
    if (a > b) {
        A = a;
        B = b;
    }
    else {
        A = b;
        B = a;
    }
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
        if (T1 < 0) {
            T1 = T1 + b;
        }
        return T1;
    }
    else {
        return -1;
    }
}

bigint calcularLambda(Ponto Q, Ponto G,bigint a,bigint p) {
    bigint lambda;
    if (pontoIgual(Q, G)) {
        lambda = divMod(addMod(mulMod(3, mulMod(Q.X, Q.X, p), p),a,p), mulMod(2, Q.Y, p), p);
    }
    else {
        lambda = divMod(subMod(G.Y, Q.Y, p), subMod(G.X, Q.X, p), p);
    }
    return lambda;
}

Ponto somaPontos(Ponto Q, Ponto G,bigint a,bigint p) {
    Ponto soma;
    if (pontoEhZero(Q)) {
        return G;
    }
    else if (pontoEhZero(G)) {
        return Q;
    }
    else if (pontoIgual(Q, negativoPonto(G, p)) || pontoIgual(G, negativoPonto(Q, p))) {
        soma.X = 0;
        soma.Y = 0;
        return soma;
    }
    else {
        bigint lambda = calcularLambda(Q, G, a, p);
        soma.X = mulMod(lambda, lambda, p);
        soma.X = subMod(soma.X, Q.X, p);
        soma.X = subMod(soma.X, G.X, p);
        soma.Y = mulMod(lambda, subMod(Q.X, soma.X, p), p);
        soma.Y = subMod(soma.Y, Q.Y, p);
        return soma;
    }
}

Ponto multiplicarPonto(Ponto Q,bigint n,bigint a,bigint p) {
    Ponto R;
    R.X = 0;
    R.Y = 0;
    for (int i = 0; i < n; i++) {
        R = somaPontos(R, Q, a, p);
    }
    return R;
}


int pontoIgual(Ponto Q, Ponto G) {
    if (Q.X == G.X && Q.Y == G.Y) {
        return 1;
    }
    else {
        return 0;
    }
}

Ponto negativoPonto(Ponto Q,bigint p) {
    Ponto negativo;
    negativo.X = Q.X;
    negativo.Y = subMod(p, Q.Y, p);
    return negativo;
}

int pontoEhZero(Ponto Q) {
    if (Q.X == 0 && Q.Y == 0) {
        return 1;
    }
    else {
        return 0;
    }
}

bigint modulo(bigint a,bigint b) {
    bigint r = a % b;
    if (r < 0) {
        r += b;
    }
    return r;
}

bigint addMod(bigint a, bigint b, bigint p) {
    return modulo((a + b), p);
}

bigint subMod(bigint a, bigint b, bigint p) {
    return modulo((a - b), p);
}

bigint mulMod(bigint a, bigint b, bigint p) {
    return modulo((a * b), p);
}

bigint divMod(bigint a, bigint b, bigint p) {
    return modulo((a * inversoModular(b, p)), p);
}