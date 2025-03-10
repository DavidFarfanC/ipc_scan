import re
from scripts.utils import luhn_checksum

def detect_credit_cards(text):
    """
    Busca posibles números de tarjeta en un texto y los valida con el algoritmo de Luhn.
    """
    pattern_card = r'(?:\d{4}[-\s]?){3}\d{4}'
    found_cards = re.findall(pattern_card, text)

    valid_cards = [card for card in found_cards if luhn_checksum(card)]
    
    return valid_cards if valid_cards else None
