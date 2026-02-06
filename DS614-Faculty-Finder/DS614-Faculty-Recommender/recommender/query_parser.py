import re

def parse_query(q):
    """
    Parse the query to extract the number of results requested and clean query text.
    
    Recognizes patterns like:
    - "top 3 machine learning"
    - "5 best computer vision"
    - "first 10 IoT experts"
    - "show me 7 VLSI faculty"
    
    Returns: (cleaned_query, number_of_results)
    """
    q_lower = q.lower()
    k = 5  # default
    
    # Pattern 1: "top N"
    m = re.search(r'\b(?:top|best|first)\s+(\d+)\b', q_lower)
    if m:
        k = int(m.group(1))
        q = re.sub(r'\b(?:top|best|first)\s+\d+\b', '', q, flags=re.IGNORECASE)
    
    # Pattern 2: "N best/top/first" or just "N faculty/professors"
    elif re.search(r'\b(\d+)\s+(?:best|top|first|faculty|faculties|professors?)\b', q_lower):
        m = re.search(r'\b(\d+)\s+(?:best|top|first|faculty|faculties|professors?)\b', q_lower)
        k = int(m.group(1))
        q = re.sub(r'\b\d+\s+(?:best|top|first|faculty|faculties|professors?)\b', '', q, flags=re.IGNORECASE)
    
    # Pattern 3: "show me N" or "give me N"
    elif re.search(r'\b(?:show|give)\s+(?:me\s+)?(\d+)\b', q_lower):
        m = re.search(r'\b(?:show|give)\s+(?:me\s+)?(\d+)\b', q_lower)
        k = int(m.group(1))
        q = re.sub(r'\b(?:show|give)\s+(?:me\s+)?\d+\b', '', q, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    q = re.sub(r'\s+', ' ', q).strip()
    
    # Ensure k is within reasonable bounds
    k = max(1, min(k, 20))
    
    return q, k

