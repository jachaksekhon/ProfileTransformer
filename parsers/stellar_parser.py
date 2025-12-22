"""
Stellar profile parser.

This module is responsible for converting Stellar AIO exported
profile JSON objects into canonical Profile objects.

Stellar JSON format (as of December 21, 2025):

{
    "profileName": "John Doe",
    "email": "email@email.com",
    "phone": "1234567890",
    "shipping": {
        "firstName": "John",
        "lastName": "Doe",
        "country": "CA",
        "address": "6767 123st",
        "address2": "",
        "state": "BC",
        "city": "Cityname",
        "zipcode": "ABC 123"
    },
    "billingAsShipping": true,
    "billing": {
        "firstName": "John",
        "lastName": "Doe",
        "country": "CA",
        "address": "6767 123st",
        "address2": "",
        "state": "BC",
        "city": "Cityname",
        "zipcode": "ABC 123"
    },
    "payment": {
        "cardName": "John Doe",
        "cardType": "Visa",
        "cardNumber": "45021111111111111",
        "cardMonth": "11",
        "cardYear": "30",
        "cardCvv": "123"
    },
    "oneCheckoutPerProfile": false
}

This module maps Stellar-specific fields to the canonical
"""

from models.canonical import Profile, Address, Card

def map_stellar_address(shipping_dic: dict) -> Address:
    return Address(
        first_name     = shipping_dic["firstName"],
        last_name      = shipping_dic["lastName"],
        address_line_1 = shipping_dic["address"],
        address_line_2 = shipping_dic["address2"],
        country        = shipping_dic["country"],
        state          = shipping_dic["state"],
        city           = shipping_dic["city"],
        zip_code       = shipping_dic["zipcode"]
    )

def map_stellar_card(card_dic: dict) -> Card:
    return Card(
        holder    = card_dic["cardName"],
        card_type = card_dic["cardType"].strip().lower(),
        number    = card_dic["cardNumber"],
        exp_month = card_dic["cardMonth"],
        exp_year  = card_dic["cardYear"],
        cvv       = card_dic["cardCvv"] 
    )


def stellar_profile_to_canonical(input_profile: dict) -> Profile:
    """
    Convert a single Stellar profile to a canonical Profile.
    """

    shipping_input = input_profile["shipping"]
    billing_input  = input_profile["billing"]
    card_input     = input_profile["payment"]
    same_billing   = input_profile["billingAsShipping"]

    shipping = map_stellar_address(shipping_input)
    billing  = shipping if same_billing else map_stellar_address(billing_input)
    card     = map_stellar_card(card_input)

    return Profile(
        profile_name         = input_profile["profileName"],
        email                = input_profile["email"],
        phone_number         = input_profile["phone"],

        shipping_address     = shipping,
        billing_address      = billing,
        billing_same_as_ship = same_billing,

        card                 = card,

        one_checkout         = input_profile["oneCheckoutPerProfile"]
    )


def map_stellar_to_canonical(stellar_profiles: list[dict]) -> list[Profile]:
    """Iterate over the input list"""
    
    return [stellar_profile_to_canonical(p) for p in stellar_profiles]
