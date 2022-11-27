import string

alfabeto = [[ch,0] for ch in string.ascii_lowercase]
texto = input("Insira um texto para contagem de frequência:\n")

for letra in texto:
    if letra in string.ascii_letters:
        letra = letra.lower()
        alfabeto[ord(letra) - 97][1] += 1

print("Ordem alfabética: ")
print(alfabeto)

alfabeto.sort(key=lambda lista_freq_letra : lista_freq_letra[1],reverse=True)

print("Ordem de maior frequência")
for parLetraFreq in alfabeto:
    print(parLetraFreq[0],end="")
print()