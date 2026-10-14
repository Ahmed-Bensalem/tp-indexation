import re
import math

# Ex1
def chargerDocuments():
    documents = {}
    with open("documents.tsv", encoding="utf-8") as file:
        next(file)
        for ligne in file:
            id, texte = ligne.strip().split("\t", 1)
            documents[id] = texte
    return documents

documents = chargerDocuments()

# Pourquoi un corpus composé de documents proches thématiquement est-il plus intéressant pour tester un algorithme de ranking ?
# -> Les documents sont similaires, donc l’algorithme doit trouver ceux qui sont les plus pertinents.


# Ex2
stopwords = {
    "a", "an", "the", "and", "or", "is", "are", "of", "to", "in",
    "for", "on", "with", "by", "as", "use", "uses", "using", "are",
    "this", "that", "it", "can", "be", "from", "into", "their"
}

def preprocess(text):
    # 1. Passage en minuscules
    text = text.lower()
    # 2. Tokenisation
    tokens = re.findall(r"\b[a-z0-9]+\b", text)
    # 3. Suppression des stopwords
    tokens = [mot for mot in tokens if mot not in stopwords]
    return tokens

#change --- to ###
print("\n--- Prétraitement de trois documents ---")
for id in ["D1", "D2", "D3"]:
    texte = documents[id]
    tokens = re.findall(r"\b[a-z0-9]+\b", texte.lower())
    tokens_sans_stopwords = [mot for mot in tokens if mot not in stopwords]
    termes = preprocess(texte)
    print("\n", id, ":", texte)
    print("Tokens :", tokens)
    print("Sans stopwords :", tokens_sans_stopwords)
    print("Termes indexés :", termes)

# Pourquoi faut-il appliquer exactement le même pipeline de prétraitement aux documents et aux requêtes ?
# -> Pour que les documents et les requêtes utilisent les mêmes termes et que les résultats soient corrects.


# Ex3
def construire_index_enrichi(documents):
    index_inverse = {}
    for doc_id, texte in documents.items():
        termes = preprocess(texte)
        for terme in termes:
            if terme not in index_inverse:
                index_inverse[terme] = {"df": 0, "postings": {}}
            if doc_id not in index_inverse[terme]["postings"]:
                index_inverse[terme]["postings"][doc_id] = {"tf": 0}
                index_inverse[terme]["df"] += 1
            index_inverse[terme]["postings"][doc_id]["tf"] += 1
    return index_inverse

index_inverse = construire_index_enrichi(documents)
N = len(documents)
vocabulary = sorted(index_inverse.keys())

print("\n--- Index inversé enrichi ---")
for terme in sorted(index_inverse):
    postings = []
    for doc_id, infos in index_inverse[terme]["postings"].items():
        postings.append(f"{doc_id}(tf={infos['tf']})")
    print(f"{terme:20} DF={index_inverse[terme]['df']:2}  {', '.join(postings)}")

# Quelle est la différence entre TF(t,d) et DF(t) ?
# -> TF = nombre d’occurrences d’un terme dans un document. 
#    DF = nombre de documents contenant ce terme.


# Ex4
def calculer_idf(terme, index_inverse, N):
    if terme not in index_inverse:
        return 0
    df = index_inverse[terme]["df"]
    return math.log10(N / df)

print("\n--- Tableau DF / IDF ---")
print(f"{'Terme':20} {'DF':>5} {'IDF':>10}")
for terme in ["information", "retrieval", "vector", "boolean"]:
    df = index_inverse[terme]["df"] if terme in index_inverse else 0
    idf = calculer_idf(terme, index_inverse, N)
    print(f"{terme:20} {df:5} {idf:10.4f}")

termes_presents = list(index_inverse.keys())
terme_df_max = max(termes_presents, key=lambda t: index_inverse[t]["df"])
terme_df_min = min(termes_presents, key=lambda t: index_inverse[t]["df"])
terme_idf_max = max(termes_presents, key=lambda t: calculer_idf(t, index_inverse, N))
print("DF maximal :", terme_df_max, "-", index_inverse[terme_df_max]["df"])
print("DF minimal :", terme_df_min, "-", index_inverse[terme_df_min]["df"])
print("IDF maximal :", terme_idf_max, "-", round(calculer_idf(terme_idf_max, index_inverse, N), 4))

# Pourquoi un terme rare dans la collection reçoit-il généralement un IDF plus élevé ?
# -> Un terme rare apparaît dans peu de documents, donc son IDF est plus élevé.


# Ex5
def poids_tfidf(terme, doc_id, index_inverse, N):
    if terme not in index_inverse:
        return 0
    postings = index_inverse[terme]["postings"]
    if doc_id not in postings:
        return 0
    tf = postings[doc_id]["tf"]
    idf = calculer_idf(terme, index_inverse, N)
    return (1 + math.log10(tf)) * idf

doc_id = "D8"
print(f"\n--- Poids TF-IDF du document {doc_id} ---")
poids_document = []
for terme in vocabulary:
    tfidf = poids_tfidf(terme, doc_id, index_inverse, N)
    if tfidf > 0:
        tf = index_inverse[terme]["postings"][doc_id]["tf"]
        df = index_inverse[terme]["df"]
        idf = calculer_idf(terme, index_inverse, N)
        poids_document.append((terme, tf, df, idf, tfidf))

poids_document.sort(key=lambda element: element[4], reverse=True)
print(f"{'TERM':20} {'TF':>4} {'DF':>4} {'IDF':>8} {'TF-IDF':>10}")
for terme, tf, df, idf, tfidf in poids_document:
    print(f"{terme:20} {tf:4} {df:4} {idf:8.4f} {tfidf:10.4f}")

# Les termes ayant le plus grand TF sont-ils toujours ceux qui ont le plus grand TF-IDF ?
# -> Non car TF-IDF dépend du TF et de l’IDF. Un terme rare peut avoir un TF-IDF plus élevé qu’un terme fréquent.


# Ex6
def document_vector(doc_id, vocabulary, index_inverse, N):
    vector = []
    for terme in vocabulary:
        vector.append(poids_tfidf(terme, doc_id, index_inverse, N))
    return vector

print("\n--- Vecteurs des documents ---")
for doc_id in ["D1", "D2", "D3"]:
    vector = document_vector(doc_id, vocabulary, index_inverse, N)
    print(doc_id, ":", vector)
    print("Nombre de composantes nulles :", vector.count(0))

# Pourquoi les vecteurs TF-IDF de documents sont-ils généralement creux (sparse) ?
# -> Chaque document utilise peu de termes du vocabulaire global, donc la plupart des valeurs du vecteur sont 0.


# Ex7
def query_vector(query, vocabulary, index_inverse, N):
    termes = preprocess(query)
    frequences = {}
    for terme in termes:
        frequences[terme] = frequences.get(terme, 0) + 1

    vector_q = []
    for terme in vocabulary:
        tf = frequences.get(terme, 0)
        if tf > 0 and terme in index_inverse:
            poids = (1 + math.log10(tf)) * calculer_idf(terme, index_inverse, N)
        else:
            poids = 0
        vector_q.append(poids)
    return vector_q

q = "information retrieval model"
vector_q = query_vector(q, vocabulary, index_inverse, N)
print("\n--- Termes non nuls de la requête ---")
for terme, poids in zip(vocabulary, vector_q):
    if poids > 0:
        print(terme, ":", round(poids, 4))

# Que doit faire le programme lorsqu’un terme de la requête n’appartient pas au vocabulaire de la collection ?
# -> Il lui attribue un poids nul, car il n’existe pas dans le vocabulaire de la collection.


# Ex8
def cosine_similarity(v1, v2):
    # 1. Produit scalaire
    produit = sum(v1[i] * v2[i] for i in range(len(v1)))
    # 2. Norme de v1
    norme1 = math.sqrt(sum(valeur ** 2 for valeur in v1))
    # 3. Norme de v2
    norme2 = math.sqrt(sum(valeur ** 2 for valeur in v2))
    # 4. Cosinus
    if norme1 == 0 or norme2 == 0:
        return 0
    return produit / (norme1 * norme2)

print("\n--- Scores cosinus de la requête ---")
for doc_id in documents:
    vector_doc = document_vector(doc_id, vocabulary, index_inverse, N)
    score = cosine_similarity(vector_q, vector_doc)
    print(doc_id, ":", round(score, 4))

# Que signifient intuitivement des scores proches de 1 et proches de 0 ?
# -> Proche de 1 indique une forte similarité. Proche de 0 indique une faible similarité.


# Ex9
def search(query, documents, index_inverse, vocabulary, N, k=5):
    vector_q = query_vector(query, vocabulary, index_inverse, N)
    results = []
    for doc_id in documents:
        vector_doc = document_vector(doc_id, vocabulary, index_inverse, N)
        score = cosine_similarity(vector_q, vector_doc)
        if score > 0:
            results.append((doc_id, score, documents[doc_id]))
    results.sort(key=lambda element: element[1], reverse=True)
    return results[:k]

def afficher_resultats(query, results):
    print("\nQuery >", query)
    print("TOP RESULTS")
    print(f"{'Rank':<6} {'DocID':<8} {'Score':<10} Document")
    print("-" * 100)
    for rang, (doc_id, score, texte) in enumerate(results, start=1):
        print(f"{rang:<6} {doc_id:<8} {score:<10.4f} {texte}")

requêtes = [
    "information retrieval model",
    "inverted index search",
    "vector documents embeddings",
    "boolean retrieval AND",
    "TF IDF ranking relevance"
]

print("\n--- Tests de cinq requêtes ---")
for requete in requêtes:
    afficher_resultats(requete, search(requete, documents, index_inverse, vocabulary, N, 5))

# 1. "information retrieval model" :
# D11 arrive premier car il contient les trois termes. D6 et D7 parlent aussi du sujet.

# 2. "inverted index search" :
# D13 arrive premier car il parle d’index inversé. D1 et D10 parlent aussi d’index et de recherche.

# 3. "vector documents embeddings" :
# D9 arrive premier grâce aux termes vector et embeddings. D8 et D2 parlent aussi des vecteurs et des embeddings.

# 4. "boolean retrieval AND" :
# D3 arrive premier car il contient les trois termes. D19 parle de recherche booléenne et D8 de recherche d’information.

# 5. "TF IDF ranking relevance" :
# D4 arrive premier car il traite du TF-IDF. D17 parle aussi du TF-IDF et D25 du classement et de la pertinence.


# Ex10
requete = "information retrieval model"

# Sans normalisation
index_sans = construire_index_enrichi(documents)
vocabulaire_sans = sorted(index_sans.keys())
resultats_sans = search(
    requete, documents, index_sans, vocabulaire_sans,
    len(documents), k=len(documents)
)

# Avec normalisation
def preprocess_normalise(text):
    tokens = preprocess(text)
    tokens = ["model" if mot == "models" else mot for mot in tokens]
    return tokens

# Le prétraitement peut-il modifier le classement final ?
# -> Oui la normalisation peut rendre « model » et « models » identiques, ce qui peut changer les scores et le classement.


# Ex11
def recherche_and(termes, index_inverse):
    listes = []
    for terme in preprocess(termes):
        if terme in index_inverse:
            listes.append(sorted(index_inverse[terme]["postings"].keys()))
        else:
            return []
    if not listes:
        return []
    resultat = listes[0]
    for liste in listes[1:]:
        resultat = intersection(resultat, liste)
    return resultat

def intersection(list1, list2):
    i, j = 0, 0
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

requete_and = "information retrieval model"
resultats_bool = recherche_and(requete_and, index_inverse)
resultats_vectoriels = search(requete_and, documents, index_inverse, vocabulary, N, 5)

print("\n--- Comparaison Booléen AND / Vectoriel TF-IDF ---")
print("Requête :", requete_and)
print("Résultats AND :", resultats_bool)
print("Résultats vectoriels :")
afficher_resultats(requete_and, resultats_vectoriels)

# - Document retrouvé : AND exige tous les termes | TF-IDF accepte une correspondance partielle.
# - Correspondance partielle : non pour AND, oui pour TF-IDF.
# - Score de pertinence : AND ne calcule pas de score ; TF-IDF utilise la similarité cosinus.
# - Classement : AND ne classe pas les résultats | TF-IDF les trie par score décroissant.

# Un document contenant seulement deux termes importants d’une requête à trois termes peut-il être retrouvé par les deux modèles de la même manière ?
# -> Non, AND exclut le document car il manque un terme. TF-IDF peut le retrouver avec un score positif grâce aux deux termes présents.


# Ex12
print("\n========================================")
print("         FIGL SEARCH ENGINE V2")
print("========================================")
print("Documents indexés :", N)
print("Taille du vocabulaire :", len(vocabulary))

while True:
    query = input("\nQuery (ou 'quit' pour arrêter) > ").strip()
    if query.lower() in ["quit", "exit", "q"]:
        break

    choix_k = input("Choisir k (3, 5 ou 10) : ").strip()
    if choix_k not in ["3", "5", "10"]:
        k = 5
    else:
        k = int(choix_k)

    results = search(query, documents, index_inverse, vocabulary, N, k)
    afficher_resultats(query, results)

# Question de synthèse : Quelles limites de TF-IDF pourraient justifier l'utilisation d'un modèle de ranking plus avancé comme BM25 ?
# -> TF-IDF a des limites liées à la longueur des documents et aux termes répétés. BM25 améliore ces points.