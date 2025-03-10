def luhn_checksum(card_number):
    """
    Implementa el Algoritmo de Luhn para validar números de tarjeta.
    """
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    dbl = False
    for d in reversed(digits):
        if dbl:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        dbl = not dbl
    return checksum % 10 == 0
