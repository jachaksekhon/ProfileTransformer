def normalize_card_number(card_number: str) -> str:
    return card_number.replace(" ", "")

def determine_card_type(card_number: str) -> str:
    """
    Determine card type (e.g: Amex, Visa) given card number
    """

    number = normalize_card_number(card_number)

    if number.startswith("4"):
        return "visa"
    
    if number.startswith(("34", "37")):
        return "amex"
    
    if number[:2] in {str(i) for i in range(51,56)}:
        return "mastercard"
    
    if 2221 <= int(number[:4]) <= 2720:
        return "mastercard"
    
    if number.startswith(("6011", "65")) or 644 <= int(number[:3]) <= 649:
        return "discover"

    if 3528 <= int(number[:4]) <= 3589:
        return "jcb"
    
    raise ValueError(f"Unable to infer card type from card number: {card_number}")