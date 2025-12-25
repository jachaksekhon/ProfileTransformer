"""
Expected stellar output:
[
  {
    "profileName": "first last",
    "email": "email@email.com",
    "phone": "1234567890",
    "shipping": 
        {
            "firstName": "John",
            "lastName": "Doe",
            "country": "CA",
            "address": "6767 123st",
            "address2": "",
            "state": "BC",
            "city": "Cityname",
            "zipcode": "ABC 123",
        },
    "billingAsShipping": true,
    "billing": { ... },
    "payment": 
        {
            "cardName": "John Doe",
            "cardType": "Visa",
            "cardNumber": "45021111111111111",
            "cardMonth": "11",
            "cardYear": "30",
            "cardCvv": "123"
        },
    "oneCheckoutPerProfile": false
  },
]

-> List of dictionaries
"""

from models.canonical import Profile, Address, Card

STELLAR_CARD_TYPE_MAP = {
    "visa": "Visa",
    "discover": "Discover",
    "mastercard": "MasterCard",
    "amex": "Amex",
    "jcb": "JCB"
}

def emit_stellar_card(card: Card) -> dict:

    if card.card_type in STELLAR_CARD_TYPE_MAP:
        stellar_card_type = STELLAR_CARD_TYPE_MAP[card.card_type]
    else:
        raise ValueError(
            f"Unsupported Stellar card type: '{card.card_type}'. "
            f"Supported types: {list(STELLAR_CARD_TYPE_MAP.values())}"
        )

    return {
        "cardName": card.holder,
        "cardType": stellar_card_type,
        "cardNumber": card.number,
        "cardMonth": card.exp_month,
        "cardYear": card.exp_year,
        "cardCvv": card.cvv
    }

def emit_stellar_shipping(address: Address) -> dict:

    return {
        "firstName": address.first_name,
        "lastName": address.last_name,
        "country": address.country_code,
        "address": address.address_line_1,
        "address2": address.address_line_2,
        "state": address.state_code,
        "city": address.city,
        "zipcode": address.zip_code,
    }

def canonical_profile_to_stellar(profile: Profile) -> dict:

    stellar_shipping = emit_stellar_shipping(profile.shipping_address)
    stellar_billing  = stellar_shipping if profile.billing_same_as_ship else emit_stellar_shipping(profile.billing_address)
    stellar_card     = emit_stellar_card(profile.card)

    return {
        "profileName": profile.profile_name,
        "email": profile.email,
        "phone": profile.phone_number,
        "shipping": stellar_shipping,
        "billingAsShipping": profile.billing_same_as_ship,
        "billing": stellar_billing,
        "payment": stellar_card,
        "oneCheckoutPerProfile": profile.one_checkout
    }



def canonical_profiles_to_stellar(profiles: list[Profile]) -> list[dict]:
    
    return [canonical_profile_to_stellar(p) for p in profiles]




