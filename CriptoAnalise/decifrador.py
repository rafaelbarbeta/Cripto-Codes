import string

def descriptografarLetra(letra,dict):
    return dict[letra]

incidencia_letras = "aeosrdnitmulcvpgqbfhjxzkyw"
chave = input("Insira a chave de frequência das letras, em ordem decrescente:\n")
decifrador = dict(zip(chave,incidencia_letras))

texto = input("Insira o texto a ser descriptografado:\n")
textoDescriptografado = ""
print("\n")
for letra in texto:
    if letra in string.ascii_letters:
        textoDescriptografado += decifrador[letra]
    elif letra != "#":
        textoDescriptografado += letra
print(textoDescriptografado)