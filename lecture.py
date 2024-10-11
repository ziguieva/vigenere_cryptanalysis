# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 00:32:18 2024

@author: evanzigui
"""


# Fonction de chiffrement Vigenère
def vigenere_chiffrement(texte_clair, cle):
    cle = cle.upper()  # Met la clé en majuscules
    longueur_cle = len(cle)
    texte_chiffre = []

    for i, caractere in enumerate(texte_clair):
        if caractere.isalpha():  # Si c'est une lettre
            decalage = ord(cle[i % longueur_cle]) - ord('A')  # Calcul du décalage
            if caractere.isupper():
                texte_chiffre.append(chr((ord(caractere) - ord('A') + decalage) % 26 + ord('A')))
            else:
                texte_chiffre.append(chr((ord(caractere) - ord('a') + decalage) % 26 + ord('a')))
        else:
            texte_chiffre.append(caractere)  # Ne modifie pas les caractères non alphabétiques
    return ''.join(texte_chiffre)

# Fonction de déchiffrement Vigenère
def vigenere_dechiffrement(texte_chiffre, cle):
    cle = cle.upper()  # Met la clé en majuscules
    longueur_cle = len(cle)
    texte_clair = []

    for i, caractere in enumerate(texte_chiffre):
        if caractere.isalpha():  # Si c'est une lettre
            decalage = ord(cle[i % longueur_cle]) - ord('A')  # Calcul du décalage
            if caractere.isupper():
                texte_clair.append(chr((ord(caractere) - ord('A') - decalage) % 26 + ord('A')))
            else:
                texte_clair.append(chr((ord(caractere) - ord('a') - decalage) % 26 + ord('a')))
        else:
            texte_clair.append(caractere)  # Ne modifie pas les caractères non alphabétiques
    return ''.join(texte_clair)

# Fonction pour lire le contenu d'un fichier
def lire_fichier(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()
    return contenu

# Fonction pour écrire le contenu dans un fichier
def ecrire_fichier(nom_fichier, contenu):
    with open(nom_fichier, 'w') as fichier:
        fichier.write(contenu)

# Fonction principale pour exécuter le chiffrement ou déchiffrement selon les arguments fournis
def vigenere(mode, fichier_in, fichier_out, cle):
    texte = lire_fichier(fichier_in)

    if mode == 'c':  # Chiffrement
        texte_chiffre = vigenere_chiffrement(texte, cle)
        ecrire_fichier(fichier_out, texte_chiffre)
        print("Chiffrement terminé. Résultat enregistré dans", fichier_out)
    elif mode == 'd':  # Déchiffrement
        texte_dechiffre = vigenere_dechiffrement(texte, cle)
        ecrire_fichier(fichier_out, texte_dechiffre)
        print("Déchiffrement terminé. Résultat enregistré dans", fichier_out)
    else:
        print("Mode inconnu. Utilisez 'c' pour chiffrer ou 'd' pour déchiffrer.")

# Appel de la fonction avec des arguments prédéfinis pour Spyder
if __name__ == "__main__":
    mode = 'c'  # 'c' pour chiffrer, 'd' pour déchiffrer
    fichier_in = 'entree.txt'  # Le fichier d'entrée
    fichier_out = 'sortie_chiffre.txt'  # Le fichier de sortie
    cle = 'CLE'  # La clé de chiffrement/déchiffrement

    vigenere(mode, fichier_in, fichier_out, cle)



