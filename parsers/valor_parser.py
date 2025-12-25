"""
Valor profile parser.

This module is responsible for converting Valor AIO exported
profile JSON objects into canonical Profile objects.

Valor JSON format (as of December 21, 2025):

{
	"unique_key_for_valor_id":
		{
			"name":"John Doe",
			"email":"email@email.com",
			"phoneNumber":"6041234567",
			"personalCustomsCode":"",
			"pinCode":"",
			"idNumber":"",
			"birthday":"",
			"billingSameAsShipping":true,
			"oneCheckout":false,
			"quickTask":false,
			"card":
				{
					"holder":"John Doe",
					"number":"3401 111111 11111",
					"expiration":"01/30",
					"cvv":"1111",
					"googlePayToken":"",
					"type":"amex"
				},
			"shipping":
				{
					"firstName":"John",
					"lastName":"Doe",
					"addressLine1":"6767 123st",
					"addressLine2":"",
					"city":"Cityname",
					"countryName":"Canada",
					"countryCode":"CA",
					"state":"Province Name",
					"zipCode":"ABC 123"
				},
			"billing":
				{
					"firstName":"John",
					"lastName":"Doe",
					"addressLine1":"6767 123st",
					"addressLine2":"",
					"city":"Cityname",
					"countryName":"Canada",
					"countryCode":"CA",
					"state":"Province Name",
					"zipCode":"ABC 123"
                },
			"id":"unique_key_for_valor_id",
			"totalSpent":0
		}
}

This module maps Valor-specific fields to the canonical
Profile, Address, and Card models for downstream transformation.
"""

from models.canonical import Profile, Address, Card
from constants.canada_provinces_map import CANADA_PROVINCE_MAP
from helpers.json_utils import require_key

def map_valor_address(shipping_dic: dict) -> Address:

    # grab shortform since valor produces expanded form
    state_name = shipping_dic["state"]

    state = CANADA_PROVINCE_MAP.get(state_name)
    if not state:
        raise ValueError(f"Unsupported Canadian province {state_name}")

    return Address(
        first_name     = shipping_dic["firstName"],
        last_name      = shipping_dic["lastName"],
        address_line_1 = shipping_dic["addressLine1"],
        address_line_2 = shipping_dic["addressLine2"],
        country        = shipping_dic["countryCode"],
        state          = state,
        city           = shipping_dic["city"],
        zip_code       = shipping_dic["zipCode"]
    )

def map_card_info(card_dic: dict) -> Card:

    month, year = card_dic["expiration"].split("/")

    return Card(
        holder    = card_dic["holder"],
        card_type = card_dic["type"].strip().lower(),
        number    = card_dic["number"],
        exp_month = month,
        exp_year  = year,
        cvv       = card_dic["cvv"] 
    )


def valor_profile_to_canonical(input_profile: dict) -> Profile:
    """Convert a single Valor profile to a canonical Profile."""

    shipping_input = input_profile["shipping"]
    billing_input  = input_profile["billing"]
    card_input     = input_profile["card"]
    same_billing   = input_profile["billingSameAsShipping"]

    shipping = map_valor_address(shipping_input)
    billing  = shipping if same_billing else map_valor_address(billing_input)
    card     = map_card_info(card_input)

    return Profile(
        profile_name         = input_profile["name"],
        email                = input_profile["email"],
        phone_number         = input_profile["phoneNumber"],

        shipping_address     = shipping,
        billing_address      = billing,
        billing_same_as_ship = same_billing,

        card                 = card,

        one_checkout         = input_profile["oneCheckout"]
    )


def map_valor_to_canonical(valor_profiles: dict) -> list[Profile]:
    """Iterate over the input list"""
    
    profiles = []

    for profile_id, profile_data in valor_profiles.items():
        profiles.append(valor_profile_to_canonical(profile_data))

    return profiles

