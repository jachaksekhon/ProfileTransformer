"""
Cybersole profile parser.

This module is responsible for converting Cybersole AIO exported 
profile JSON objects into canonical Profile objects.

Cybersole JSON format (as of December 26, 2025):

[
	{
		"id":"123456",
		"name":"Group 1",
		"profiles":[
			{
				"id":"6b654e25",
				"name":"John Pork",
				"email":"email@email.com",
				"phone":"4165848583",
				"billingDifferent":false,
				"card":
                    {
                        "number":"1234 1237 1237 1237",
                        "expMonth":"01",
                        "expYear":"2022",
                        "cvv":"132"
					},
				"delivery":
					{
						"firstName":"John",
						"lastName":"Pork",
						"address1":"123 Jac Street",
						"address2":null,
						"city":"ASD city",
						"zip":"4737",
						"country":"Canada",
						"state":"Ontario"
					},
				"billing":
					{
						"firstName":null,
						"lastName":null,
						"address1":null,
						"address2":null,
						"city":null,
						"zip":null,
						"country":null,
						"state":null
					},
				"properties":{}
			}
		]
	}
]

This module maps Cybersole-specific fields to the canonical
"""

from models.canonical import Profile, Card, Address
from helpers.json_utils import require_key

import constants.countries_map as countries_helper
import helpers.card_utils as card_util

def map_cybersole_card(card_dict: dict, profile_holder_name: str) -> Card:

    card_number   = require_key(card_dict, "number", "cybersole card number")
    card_type     = card_util.determine_card_type(card_number)
    exp_year_full = require_key(card_dict, "expYear", "cybersole card expiry year")

    return Card(
        holder    = profile_holder_name,
        card_type = card_type,
        number    = card_number,
        exp_month = require_key(card_dict, "expMonth", "cybersole expiry month"),
        exp_year  = exp_year_full[-2:], # passed in as 4 digits, only need last 2
        cvv       = require_key(card_dict, "cvv", "cybersole card cvv"),
    )

def map_cybersole_address(shipping_dic: dict) -> Address:

    country_name = require_key(shipping_dic, "country", "cybersole shipping country name")
    country_code = countries_helper.COUNTRY_NAME_TO_CODE_MAP[country_name]

    state_or_province_name = require_key(shipping_dic, "state", "cybersole shipping state name")
    state_or_province_code = countries_helper.province_or_state_code_finder(country_code, state_or_province_name)
    
    return Address(
        first_name     = require_key(shipping_dic, "firstName", "cybersole shipping first name"),
        last_name      = require_key(shipping_dic, "lastName", "cybersole shipping last name"),
        address_line_1 = require_key(shipping_dic, "address1", "cybersole shipping address 1"),
        address_line_2 = shipping_dic.get("address2", ""),
        country_name   = country_name,
        country_code   = country_code,
        state_name     = state_or_province_name,
        state_code     = state_or_province_code,
        city           = require_key(shipping_dic, "city", "cybersole shipping city"),
        zip_code       = require_key(shipping_dic, "zip", "cybersole shipping zipcode"),
    )

def cybersole_profile_to_canonical(input_profile: dict) -> Profile:
    """
    Convert a single cybersole profile to a canonical Profile.
    """
    profile_holder_name = require_key(input_profile, "name", "cybersole profile name")

    shipping_input      = require_key(input_profile, "delivery", "cybersole shipping key")
    billing_input       = require_key(input_profile, "billing", "cybersole billing key")
    card_input          = require_key(input_profile, "card", "cybersole payment key")
    billing_different   = require_key(input_profile, "billingDifferent", "cybersole same ship key")

    shipping = map_cybersole_address(shipping_input)
    billing  = shipping if not billing_different else map_cybersole_address(billing_input)
    card     = map_cybersole_card(card_input, profile_holder_name)

    return Profile(
        profile_name         = profile_holder_name,
        email                = require_key(input_profile, "email", "cybersole profile email"),
        phone_number         = require_key(input_profile, "phone", "cybersole profile phone"),

        shipping_address     = shipping,
        billing_address      = billing,
        billing_same_as_ship = not billing_different, # false value here is true in canonical

        card                 = card
    )

def map_cybersole_to_canonical(cybersole_profile_json: list[dict]) -> list[Profile]:
    """
    Iterate over the input list of cybersole profiles.
    """
    profiles = []

    for group in cybersole_profile_json:
        for profile in require_key(group, "profiles", "cybersole group profiles"):
            profiles.append(cybersole_profile_to_canonical(profile))

    return profiles