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
from helpers.json_utils import require_key
import constants.countries_map as countries_helper

def map_valor_address(shipping_dic: dict) -> Address:

    country_code = require_key(shipping_dic, "countryCode", "valor shipping country")
    country_name = countries_helper.find_country_from_code(country_code)

    province_or_state_name = require_key(shipping_dic, "state", "valor shipping state/province")
    province_or_state_code = countries_helper.province_or_state_code_finder(country_code, province_or_state_name)

    return Address(
        first_name     = require_key(shipping_dic, "firstName", "valor shipping first name"),
        last_name      = require_key(shipping_dic, "lastName", "valor shipping last name"),
        address_line_1 = require_key(shipping_dic, "addressLine1", "valor shipping address"),
        address_line_2 = require_key(shipping_dic, "addressLine2", "valor shipping address2"),
        country_name   = country_name,
        country_code   = country_code,
        state_name     = province_or_state_name,
        state_code     = province_or_state_code,
        city           = require_key(shipping_dic, "city", "valor shipping city"),
        zip_code       = require_key(shipping_dic, "zipCode", "valor shipping zipcode"),
    )

def map_card_info(card_dic: dict) -> Card:

    # Valor stores month/year: E.g 02/12
    month, year = require_key(card_dic, "expiration", "valor card expiry").split("/")

    return Card(
        holder    = require_key(card_dic, "holder", "valor card holder name"),
        card_type = require_key(card_dic, "type", "valor card type").strip().lower(),
        number    = require_key(card_dic, "number", "valor card type").replace(" ", ""),
        exp_month = month,
        exp_year  = year,
        cvv       = require_key(card_dic, "cvv", "valor card cvv") 
    )


def valor_profile_to_canonical(input_profile: dict) -> Profile:
    """
    Convert a single Valor profile to a canonical Profile.
    """

    shipping_input = require_key(input_profile, "shipping", "valor shipping key")
    billing_input  = require_key(input_profile, "billing", "valor billing key")
    card_input     = require_key(input_profile, "card", "valor card key")
    same_billing   = require_key(input_profile, "billingSameAsShipping", "valor billingSameAsShipping key")

    shipping = map_valor_address(shipping_input)
    billing  = shipping if same_billing else map_valor_address(billing_input)
    card     = map_card_info(card_input)

    return Profile(
        profile_name         = require_key(input_profile, "name", "valor profile name"),
        email                = require_key(input_profile, "email", "valor profile email"),
        phone_number         = require_key(input_profile, "phoneNumber", "valor profile phone number"),

        shipping_address     = shipping,
        billing_address      = billing,
        billing_same_as_ship = same_billing,

        card                 = card,

        one_checkout         = require_key(input_profile, "oneCheckout", "valor profile onecheckout")
    )


def map_valor_to_canonical(valor_profiles: dict) -> list[Profile]:
    """
    Iterate over the input list of Valor profiles.
    """
    
    profiles = []

    for profile_id, profile_data in valor_profiles.items():
        profiles.append(valor_profile_to_canonical(profile_data))

    return profiles

