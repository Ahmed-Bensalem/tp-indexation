# Complexité : O(D × M)
def chargerDocuments():
    documents = {}
    with open("TP2/documents.txt", encoding="utf-8") as file:
        for ligne in file:
            ligne = ligne.strip()
            if ligne:
                id, texte = ligne.split(":", 1)
                documents[id.strip()] = texte.strip()
    return documents

documents = chargerDocuments()

print(documents)

def formatId(id):
    id = id.strip()
    return id[3:] if (id.startswith("d") or id.startswith("D")) else id

def construireIndex(documents):
    index_inverse = {}
    for id, texte in documents.items():
        mots = texte.lower().split()
        for mot in mots:
            if mot not in index_inverse:
                index_inverse[mot] = []
            index_inverse[mot].append(formatId(id))
    for mot in index_inverse:
        index_inverse[mot].sort()
    return index_inverse

index_inverse = construireIndex(documents)

print("index_inverse = ", index_inverse)


# Complexité : O(n + m)
def intersection(list1, list2):
    i,j = 0, 0
    result = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return result


# Complexité : O(n)
def construireSauts(liste):
    sauts = {}
    pas = int(len(liste) ** 0.5)

    if pas == 0:
        return sauts

    i = 0
    while i + pas < len(liste):
        sauts[i] = i + pas
        i += pas

    return sauts


# Complexité : O(n + m) dans le pire cas
def intersectionAvecSauts(list1, list2, sauts1, sauts2):
    i,j = 0, 0
    result = []

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            if i in sauts1 and list1[sauts1[i]] <= list2[j]:
                i = sauts1[i]
            else:
                i += 1
        else:
            if j in sauts2 and list2[sauts2[j]] <= list1[i]:
                j = sauts2[j]
            else:
                j += 1

    return result


# Test 1
terme1_test = "maison"
terme2_test = "belle"

docs1_test = index_inverse.get(terme1_test, [])
docs2_test = index_inverse.get(terme2_test, [])

sauts1_test = construireSauts(docs1_test)
sauts2_test = construireSauts(docs2_test)

print("\nTest 1 : maison et belle")
print("Liste 1 :", docs1_test)
print("Liste 2 :", docs2_test)
print("Sauts 1 :", sauts1_test)
print("Sauts 2 :", sauts2_test)
print("Intersection :", intersection(docs1_test, docs2_test))
print("Intersection avec sauts :", intersectionAvecSauts(docs1_test, docs2_test, sauts1_test, sauts2_test))


# Test 2
terme1_test = "chat"
terme2_test = "jardin"

docs1_test = index_inverse.get(terme1_test, [])
docs2_test = index_inverse.get(terme2_test, [])

sauts1_test = construireSauts(docs1_test)
sauts2_test = construireSauts(docs2_test)

print("\nTest 2 : chat et jardin")
print("Liste 1 :", docs1_test)
print("Liste 2 :", docs2_test)
print("Sauts 1 :", sauts1_test)
print("Sauts 2 :", sauts2_test)
print("Intersection :", intersection(docs1_test, docs2_test))
print("Intersection avec sauts :", intersectionAvecSauts(docs1_test, docs2_test, sauts1_test, sauts2_test))


# Test 3
terme1_test = "chien"
terme2_test = "maison"

docs1_test = index_inverse.get(terme1_test, [])
docs2_test = index_inverse.get(terme2_test, [])

sauts1_test = construireSauts(docs1_test)
sauts2_test = construireSauts(docs2_test)

print("\nTest 3 : chien et maison")
print("Liste 1 :", docs1_test)
print("Liste 2 :", docs2_test)
print("Sauts 1 :", sauts1_test)
print("Sauts 2 :", sauts2_test)
print("Intersection :", intersection(docs1_test, docs2_test))
print("Intersection avec sauts :", intersectionAvecSauts(docs1_test, docs2_test, sauts1_test, sauts2_test))


# Test 4
terme1_test = "terrasse"
terme2_test = "garage"

docs1_test = index_inverse.get(terme1_test, [])
docs2_test = index_inverse.get(terme2_test, [])

sauts1_test = construireSauts(docs1_test)
sauts2_test = construireSauts(docs2_test)

print("\nTest 4 : terrasse et garage")
print("Liste 1 :", docs1_test)
print("Liste 2 :", docs2_test)
print("Sauts 1 :", sauts1_test)
print("Sauts 2 :", sauts2_test)
print("Intersection :", intersection(docs1_test, docs2_test))
print("Intersection avec sauts :", intersectionAvecSauts(docs1_test, docs2_test, sauts1_test, sauts2_test))


# Test 5
terme1_test = "ordinateur"
terme2_test = "maison"

docs1_test = index_inverse.get(terme1_test, [])
docs2_test = index_inverse.get(terme2_test, [])

sauts1_test = construireSauts(docs1_test)
sauts2_test = construireSauts(docs2_test)

print("\nTest 5 : ordinateur et maison")
print("Liste 1 :", docs1_test)
print("Liste 2 :", docs2_test)
print("Sauts 1 :", sauts1_test)
print("Sauts 2 :", sauts2_test)
print("Intersection :", intersection(docs1_test, docs2_test))
print("Intersection avec sauts :", intersectionAvecSauts(docs1_test, docs2_test, sauts1_test, sauts2_test))