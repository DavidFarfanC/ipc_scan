import re

def detect_curp(text):
    """
    Busca CURPs en un texto usando una expresión regular.
    """
    pattern_curp = r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]{2}\b'
    found_curps = re.findall(pattern_curp, text)
    
    return found_curps if found_curps else None
