import math

def cosine(v1, v2):
    common = set(v1) & set(v2)

    num = sum(v1[w]*v2[w] for w in common)

    d1 = math.sqrt(sum(x*x for x in v1.values()))
    d2 = math.sqrt(sum(x*x for x in v2.values()))

    if d1 == 0 or d2 == 0:
        return 0

    return num/(d1*d2)
