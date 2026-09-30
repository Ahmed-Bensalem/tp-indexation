import re
import time

# Exercice 1 — Chargement des documents
def chargerDocuments():
    documents = {}
    with open('./documents.tsv', encoding='utf-8') as file:
        next(file)
        for ligne in file:
            id, texte = ligne.strip().split('\t')
            documents[id] = texte
    return documents

documents = chargerDocuments()
print(f"Nombre de documents chargés : {len(documents)}")

# Exercice 2 — Recherche naïve
def recherche_naive(terme, documents):
    resultats = []
    for id, texte in documents.items():
        if terme.lower() in texte.lower():
            resultats.append(id)
    return resultats

# Complexité : O(n), n = nombre de documents.

terme = input("Entrez un terme : ")
print(recherche_naive(terme, documents))

# Questions
# 1. Combien de documents sont parcourus pour traiter une requête ?
# Réponse : Tous les documents sont parcourus.
#
# 2. Que se passe-t-il si la collection contient 10 000 000 de documents ?
# Réponse : Les 10 000 000 de documents sont parcourus, donc la recherche devient très lente.
#
# 3. Si l'on effectue 1 000 requêtes, doit-on reparcourir les documents 1 000 fois ?
# Réponse : Oui, les documents sont parcourus pour chaque requête.
#
# 4. Quelle structure de données pourrait éviter ce parcours répétitif ?
# Réponse : Un index inversé.

# Exercice 3 — Prétraitement
# 3.1 Tokenisation
def tokeniser(texte):
    return re.findall(r"\b\w+\b", texte.lower())

# Complexité : O(m), m = longueur du texte.

print(tokeniser(documents["D1"]))

# 3.2 Suppression des mots vides
stopwords = {
    "le", "la", "les", "un", "une",
    "de", "des", "du", "et", "dans",
    "par", "pour", "d", "l"
}

def supprimer_stopwords(tokens):
    return [mot for mot in tokens if mot not in stopwords]

# Complexité : O(n), n = nombre de tokens.

tokens = tokeniser(documents["D1"])
print(tokens)
tokens_sans_stopwords = supprimer_stopwords(tokens)
print(tokens_sans_stopwords)

# Exercice 4 — Création des termes d'indexation
def preprocess(texte):
    tokens = tokeniser(texte)
    tokens = supprimer_stopwords(tokens)
    return tokens

for id, texte in documents.items():
    termes = preprocess(texte)
    print(id, ":", termes)

# Exercice 5 — Construction de l'index inversé
def construire_index(documents):
    index_inverse = {}
    for doc_id, texte in documents.items():
        termes = preprocess(texte)
        for terme in set(termes):
            if terme not in index_inverse:
                index_inverse[terme] = []
            index_inverse[terme].append(doc_id)
    return index_inverse

# Complexité : O(N × m), N = nombre de documents et m = nombre de termes par document.

index_inverse = construire_index(documents)
for terme in sorted(index_inverse):
    print(terme, "->", index_inverse[terme])

# Exercice 6 — Recherche avec l'index inversé
def rechercher(terme, index_inverse):
    return index_inverse.get(terme.lower(), [])

# Complexité : O(1) en moyenne avec un dictionnaire.

terme = input("Entrez un terme : ")
print("Recherche naïve :", recherche_naive(terme, documents))
print("Recherche avec index :", rechercher(terme, index_inverse))

# Tests de recherche avec plusieurs termes
print("\n--- Tests de recherche ---")
for terme in ["recherche", "documents", "moteur", "indexation", "intelligence"]:
    print(terme, "->", recherche_naive(terme, documents))

# Exercice 7 — Intersection
def intersection(list1, list2):
    i = 0
    j = 0
    resultat = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            resultat.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return resultat

# Complexité : O(n + m), n et m = tailles des deux listes.

terme1 = input("Entrez le premier terme : ").lower()
terme2 = input("Entrez le deuxième terme : ").lower()
docs1 = index_inverse.get(terme1, [])
docs2 = index_inverse.get(terme2, [])
print("Intersection :", intersection(docs1, docs2))

# Tests de requêtes AND
print("\n--- Tests AND ---")
tests_and = [
    ("recherche", "documents"),
    ("moteur", "recherche"),
    ("moteurs", "recherche")
]

for terme1, terme2 in tests_and:
    docs1 = index_inverse.get(terme1, [])
    docs2 = index_inverse.get(terme2, [])
    print(terme1, "AND", terme2, "->", intersection(docs1, docs2))

# Exercice 8 — Comparaison expérimentale
for taille in [100, 1000, 10000]:
    documents_test = {}
    for i in range(1, taille + 1):
        documents_test["D" + str(i)] = documents["D" + str((i - 1) % 10 + 1)]

    index_test = construire_index(documents_test)

    debut = time.perf_counter()
    recherche_naive("recherche", documents_test)
    fin = time.perf_counter()
    temps_naive = fin - debut

    debut = time.perf_counter()
    rechercher("recherche", index_test)
    fin = time.perf_counter()
    temps_index = fin - debut

    print(taille, "documents")
    print("Recherche naïve :", temps_naive, "secondes")
    print("Recherche indexée :", temps_index, "secondes")