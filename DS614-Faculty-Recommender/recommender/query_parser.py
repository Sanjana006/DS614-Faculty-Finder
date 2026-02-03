import re

def parse_query(q):
    q = q.lower()

    m = re.search(r'top\s+(\d+)', q)
    k = int(m.group(1)) if m else 5

    q = re.sub(r'top\s+\d+', '', q)
    return q.strip(), k
