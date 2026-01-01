"""
Expected cybersole output:
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

-> List of dictionaries
"""

from models.canonical import Profile, Address, Card
import helpers.card_utils as card_helper
import uuid

def emit_cybersole_card(card: Card) -> dict:

	card_number      = card_helper.formatted_card_number(card.number, card.card_type)
	card_year_expiry = card_helper.CARD_EXPIRY_YEAR_PREFIX + card.exp_year
	
	return {
		"number": card_number,
		"expMonth": card.exp_month,
		"expYear": card_year_expiry,
        "cvv": card.cvv
	}

def emit_cybersole_shipping(address: Address) -> dict:
	
	return {
		"firstName": address.first_name,
		"lastName": address.last_name,
		"address1": address.address_line_1,
		"address2": address.address_line_2 or None, # cybersole expects None not empty strings
		"city": address.city,
		"zip": address.zip_code,
		"country": address.country_name,
		"state": address.state_name
	}

def canonical_profile_to_cybersole(profile: Profile) -> dict:

	same_billing     = profile.billing_same_as_ship

	card             = emit_cybersole_card(profile.card)
	shipping_address = emit_cybersole_shipping(profile.shipping_address)
	billing_address  = shipping_address if same_billing else emit_cybersole_shipping(profile.billing_address)

	return {
		"id": str(uuid.uuid4()),
		"name": profile.profile_name,
		"email": profile.email,
		"phone": profile.phone_number,
		"billingDifferent": not same_billing,

		"card": card,
		"delivery": shipping_address,
		"billing": billing_address,

		"properties": {}
	}


def canonical_profiles_to_cybersole(profiles: list[Profile]) -> list[dict]:
	return [
		{
			"id": str(uuid.uuid4()),
			"name": "ProfileTransformer Import",
			"profiles": [canonical_profile_to_cybersole(p) for p in profiles]
		}
	]