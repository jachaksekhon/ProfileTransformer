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
from helpers.json_utils import require_key
import constants.countries_map as countries_helper


def map_stellar_address(shipping_dic: dict) -> Address:

    country_code = require_key(shipping_dic, "country", "stellar shipping country") # e.g. "CA"
    country_name = countries_helper.find_country_from_code(country_code)

    state_or_province_code = require_key(shipping_dic, "state", "stellar shipping state/province")
    state_or_province_name = countries_helper.province_or_state_code_finder(country_code, state_or_province_code)

    return Address(
        first_name     = require_key(shipping_dic, "firstName", "stellar shipping first name"),
        last_name      = require_key(shipping_dic, "lastName", "stellar shipping last name"),
        address_line_1 = require_key(shipping_dic, "address", "stellar shipping address"),
        address_line_2 = shipping_dic.get("address2", ""),
        country_name   = country_name,
        country_code   = country_code,
        state_name     = state_or_province_name,
        state_code     = state_or_province_code,
        city           = require_key(shipping_dic, "city", "stellar shipping city"),
        zip_code       = require_key(shipping_dic, "zipcode", "stellar shipping zipcode"),
    )

def map_stellar_card(card_dic: dict) -> Card:
    return Card(
        holder    = require_key(card_dic, "cardName", "stellar card holder"),
        card_type = require_key(card_dic, "cardType", "stellar card type").strip().lower(), # e.g "visa", "amex"
        number    = require_key(card_dic, "cardNumber", "stellar card number"),
        exp_month = require_key(card_dic, "cardMonth", "stellar card month"),
        exp_year  = require_key(card_dic, "cardYear", "stellar card year"),
        cvv       = require_key(card_dic, "cardCvv", "stellar card cvv") 
    )

def stellar_profile_to_canonical(input_profile: dict) -> Profile:
    """
    Convert a single Stellar profile to a canonical Profile.
    """

    shipping_input = require_key(input_profile, "shipping", "stellar shipping key")
    billing_input  = require_key(input_profile, "billing", "stellar billing key")
    card_input     = require_key(input_profile, "payment", "stellar payment key")
    same_billing   = require_key(input_profile, "billingAsShipping", "stellar same ship key")

    shipping = map_stellar_address(shipping_input)
    billing  = shipping if same_billing else map_stellar_address(billing_input)
    card     = map_stellar_card(card_input)

    return Profile(
        profile_name         = require_key(input_profile, "profileName", "stellar profile name"),
        email                = require_key(input_profile, "email", "stellar profile email"),
        phone_number         = require_key(input_profile, "phone", "stellar profile phone number"),

        shipping_address     = shipping,
        billing_address      = billing,
        billing_same_as_ship = same_billing,

        card                 = card,

        one_checkout         = require_key(input_profile, "oneCheckoutPerProfile", "stellar profile onecheckout"),
    )

def map_stellar_to_canonical(stellar_profiles: list[dict]) -> list[Profile]:
    """
    Iterate over the input list of Stellar profiles.
    """
    
    return [stellar_profile_to_canonical(p) for p in stellar_profiles]
