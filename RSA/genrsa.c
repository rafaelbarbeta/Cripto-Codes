#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h>


// Comando de compilação : gcc -o genrsa genrsa.c -lgmp

int main() {
    long long int llseed;
    int tam_chave;
    FILE *sysRandom;
    mpz_t p,q,n,e,d,phi_n;
    mpz_t auxp,auxq, auxgcd;
    mpz_t mseed;
    mpz_init(p);
    mpz_init(q);
    mpz_init(n);
    mpz_init(e);
    mpz_init(d);
    mpz_init(phi_n);
    mpz_init(mseed);
    mpz_init(auxgcd);
    mpz_init(auxp);
    mpz_init(auxq);
    printf("Digite o tamanho da chave: ");
    scanf("%d",&tam_chave);
    // Usa o arquivo especial do sistema Unix "urandom" para gerar uma seed segura
    sysRandom = fopen("/dev/urandom","rb");
    if (sysRandom != NULL) {   
        fread(&llseed,1,sizeof(llseed),sysRandom);
        fclose(sysRandom);
    }
    // Para windows, utiliza a função insegura rand para gerar os números
    else {
        srand(time(NULL));
        llseed = rand();
    }
    mpz_set_ui(mseed,llseed);
    gmp_randstate_t state;
    gmp_randinit_default(state);
    gmp_randseed(state,mseed);
    // Gera o primeiro primo. Gera um número e testa primalidade, se não for primo, gera outro
    mpz_urandomb(p,state,tam_chave);
    while (mpz_probab_prime_p(p,30) == 0) {
        mpz_urandomb(p,state,tam_chave/2);
    }
    // Repete o processo para o segundo primo
    mpz_urandomb(q,state,tam_chave);
    while (mpz_probab_prime_p(q,30) == 0) {
        mpz_urandomb(q,state,tam_chave/2);
    }
    // Calcula n = p*q
    mpz_mul(n,p,q);
    // Calcula phi(n) = (p-1)*(q-1)
    mpz_sub_ui(auxp,p,1);
    mpz_sub_ui(auxq,q,1);
    mpz_mul(phi_n,auxp,auxq);
    
    // Geração do expoente público e. Escolhe um número aleatório e testa se é coprimo com phi(n) no intervalo [2,phi(n)-1]
    mpz_urandomm(e,state,phi_n);
    mpz_gcd(auxgcd,e,phi_n);
    while (mpz_cmp_ui(e,1) <= 0 || mpz_cmp_ui(auxgcd,1) != 0) {
        mpz_urandomm(e,state,phi_n);
        mpz_gcd(auxgcd,e,phi_n);
    }

    // Calcula o expoente privado d = e^-1 mod phi(n). Utiliza o algoritmo de Euclides estendido
    mpz_t A, B, T1, T2, Q, R, T;
    mpz_t aux;
    mpz_init(A);
    mpz_init(B);
    mpz_init(T1);
    mpz_init(T2);
    mpz_init(Q);
    mpz_init(R);
    mpz_init(T);
    mpz_init(aux);
    mpz_set_ui(T1,0);
    mpz_set_ui(T2,1);

    if (mpz_cmp(e,phi_n) > 0) {
        mpz_set(A,e);
        mpz_set(B,phi_n);
    }
    else {
        mpz_set(A,phi_n);
        mpz_set(B,e);
    }
    while (mpz_cmp_ui(B,0) > 0) {
        mpz_fdiv_q(Q,A,B);
        mpz_mod(R,A,B);
        mpz_mul(aux,T2,Q);
        mpz_sub(T,T1,aux);
        mpz_set(A,B);
        mpz_set(B,R);
        mpz_set(T1,T2);
        mpz_set(T2,T);
    }
    mpz_set(d,T1);
    // O inverso modular deve ser um valor positivo
    if (mpz_cmp_ui(T1,0) < 0) {
        mpz_add(d,d,phi_n);
    }

    // Imprime os resultados em base 16, respectivamente: n,e,d,p,q
    printf("BASE: 16\n");
    gmp_printf("n = %Zx\n",n);
    gmp_printf("e = %Zx\n",e);
    gmp_printf("d = %Zx\n",d);
    gmp_printf("p = %Zx\n",p);
    gmp_printf("q = %Zx\n",q);

    /* Teste de funcionamento da chave
    mpz_t m,c,dm;
    mpz_init(m);
    mpz_init(c);
    mpz_init(dm);
    mpz_set_ui(m,738590274245612);
    gmp_printf("Mensagem = %Zx\n",m);
    // Cifra a mensagem
    mpz_powm(c,m,e,n);
    gmp_printf("Cifra = %Zx\n",c);
    // Decifra a mensagem
    mpz_powm(dm,c,d,n);
    gmp_printf("Decifra = %Zx\n",dm);
    if (mpz_cmp(dm,m) == 0) {
        printf("Chave funcionando corretamente!\n");
    }
    else {
        printf("Chave não funcionando corretamente!\n");
    }
    */
    return 0;
}
