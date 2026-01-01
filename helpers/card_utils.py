CARD_EXPIRY_YEAR_PREFIX = "20"

def normalize_card_number(card_number: str) -> str:
    """
    Removes spaces from a card number.
    """
    return card_number.replace(" ", "")

def determine_card_type(card_number: str) -> str:
    """
    Determine card type (e.g: Amex, Visa) given card number

    Returns:
        One of: 'visa', 'mastercard', 'amex', 'discover', 'jcb'
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

def formatted_card_number(card_number: str, card_type: str) -> str:
    """
    Method which adds appropriate spacing to canonical card number
    depending on the card type.

    Canonical card_number should be a continguous string

    Amex cards (15 digits): #### ###### #####
    Other types (16 digits): #### #### #### ####
    """
    
    if card_type == "amex":
        if len(card_number) != 15:
            raise ValueError("Amex cards must have a length of 15 digits")
        return f"{card_number[:4]} {card_number[4:10]} {card_number[10:]}"
    
    if len(card_number) != 16:
        raise ValueError(f"{card_type.upper()} card numbers must be 16 digits")
    
    return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"

def formatted_card_expiry_date(month: str, year: str) -> str:
    """
    Takes in expiry month and year (as 2 digits) 
    and returns the joined month/year

    return e.g: "02/25"
    """

    return month + "/" + year