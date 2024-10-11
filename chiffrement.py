# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 00:49:17 2024

@author: evanzigui
"""

from collections import Counter



# Fonction pour lire le contenu d'un fichier
def lire_fichier(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()
    return contenu

# Fonction pour écrire le contenu dans un fichier
def ecrire_fichier(nom_fichier, contenu):
    with open(nom_fichier, 'w') as fichier:
        fichier.write(contenu)

# Fonction pour calculer l'indice de coïncidence d'une chaîne de caractères
def indice_coincidence(texte):
    frequence = Counter(texte)
    n = len(texte)
    if n <= 1:
        return 0
    ic = sum(f * (f - 1) for f in frequence.values()) / (n * (n - 1))
    return ic

# Fonction pour extraire les sous-chaînes correspondant à une longueur de clé
def extraire_sous_messages(texte, longueur_cle):
    sous_messages = ['' for _ in range(longueur_cle)]
    for i, caractere in enumerate(texte):
        sous_messages[i % longueur_cle] += caractere
    return sous_messages

# Fonction pour trouver le décalage en supposant que la lettre la plus fréquente correspond à 'E'
def trouver_decalage(sous_message):
    frequence = Counter(sous_message)
    lettre_freq = frequence.most_common(1)[0][0]  # Lettre la plus fréquente
    decalage = (ord(lettre_freq) - ord('E')) % 26  # Décalage par rapport à 'E'
    return decalage

# Fonction de déchiffrement Vigenère
def vigenere_dechiffrement(texte_chiffre, cle):
    cle = cle.upper()  # Clé en majuscules
    longueur_cle = len(cle)
    texte_clair = []

    for i, caractere in enumerate(texte_chiffre):
        if caractere.isalpha():  # Si c'est une lettre
            decalage = ord(cle[i % longueur_cle]) - ord('A')  # Calcul du décalage à partir de la clé
            if caractere.isupper():
                texte_clair.append(chr((ord(caractere) - ord('A') - decalage) % 26 + ord('A')))
            else:
                texte_clair.append(chr((ord(caractere) - ord('a') - decalage) % 26 + ord('a')))
        else:
            texte_clair.append(caractere)  # Ne modifie pas les caractères non alphabétiques
    return ''.join(texte_clair)

# Fonction pour calculer la clé probable en analysant les sous-messages
def extraire_cle_probable(sous_messages):
    cle_probable = []
    
    for sous_message in sous_messages:
        decalage = trouver_decalage(sous_message)
        # Convertir le décalage en lettre correspondante
        cle_probable.append(chr((decalage + ord('A')) % 26 + ord('A')))
    
    return ''.join(cle_probable)

# Appel de la fonction de déchiffrement avec la clé probable
def decrypter_avec_cle_probable(fichier_chiffre, fichier_sortie, cle_probable):
    # Lire le fichier chiffré
    texte_chiffre = lire_fichier(fichier_chiffre)
    
    # Déchiffrer avec la clé probable
    texte_dechiffre = vigenere_dechiffrement(texte_chiffre, cle_probable)
    
    # Sauvegarder le texte déchiffré dans un fichier de sortie
    ecrire_fichier(fichier_sortie, texte_dechiffre)
    
    print(f"Texte déchiffré avec la clé probable '{cle_probable}' sauvegardé dans {fichier_sortie}")
    return texte_dechiffre

# Fonction de cryptanalyse utilisant la méthode de Kasiski
def kasiski(fichier_in, longueur_max_cle=10):
    # Lire le fichier contenant le texte chiffré
    texte = lire_fichier(fichier_in)
    
    # Filtrer les caractères pour ne garder que les lettres
    texte_filtre = ''.join([c for c in texte if c.isalpha()])

    # Stocker les résultats des indices de coïncidence pour chaque longueur de clé testée
    resultats_ic = []

    # Tester les longueurs de clé possibles (jusqu'à longueur_max_cle)
    for longueur in range(1, longueur_max_cle + 1):
        sous_messages = extraire_sous_messages(texte_filtre, longueur)
        ic_moyen = sum(indice_coincidence(sous_texte) for sous_texte in sous_messages) / longueur
        resultats_ic.append((longueur, ic_moyen))

    # Trouver la longueur de clé la plus probable (celle qui maximise l'IC)
    longueur_probable = max(resultats_ic, key=lambda x: x[1])[0]
    print(f"Longueur probable de la clé : {longueur_probable}")

    # Extraire les sous-messages pour la longueur probable de clé
    sous_messages_probables = extraire_sous_messages(texte_filtre, longueur_probable)

    # Affichage des sous-messages pour cryptanalyse plus poussée
    for i, sous_message in enumerate(sous_messages_probables):
        print(f"Sous-message {i+1}: {sous_message[:30]}...")

    # Calculer la clé probable en analysant les sous-messages
    cle_probable = extraire_cle_probable(sous_messages_probables)
    print(f"Clé probable : {cle_probable}")
    
    # Appeler la fonction de déchiffrement avec la clé probable
    fichier_sortie = 'sortie_dechiffre.txt'
    decrypter_avec_cle_probable(fichier_in, fichier_sortie, cle_probable)

    
    # Retourner la longueur probable et les sous-messages
    return longueur_probable, sous_messages_probables, cle_probable

# Exécution de la la cryptanalyse 
if __name__ == "__main__":
    fichier_in = 'sortie_chiffre.txt'  # Le fichier chiffré
    longueur_max_cle = 10  # Longueur maximale de clé à tester
    kasiski(fichier_in, longueur_max_cle)
