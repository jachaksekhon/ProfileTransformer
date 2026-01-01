"""
Expected valor output:
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

-> Excepts a single dictionary object, with keys being unique IDs
"""
import uuid
import helpers.card_utils as card_helper

from models.canonical import Profile, Address, Card

def emit_valor_card(card: Card) -> dict:
    
    return {
        "holder": card.holder,
        "number": card_helper.formatted_card_number(card.number, card.card_type),
        "expiration": card_helper.formatted_card_expiry_date(card.exp_month, card.exp_year),
        "cvv": card.cvv,
        "googlePayToken":"",
        "type": card.card_type
    }

def emit_valor_shipping(shipping_address: Address) -> dict:
    
    return {
        "firstName": shipping_address.first_name,
        "lastName": shipping_address.last_name,
        "addressLine1": shipping_address.address_line_1,
        "addressLine2": shipping_address.address_line_2,
        "city": shipping_address.city,
        "countryName": shipping_address.country_name,
        "countryCode": shipping_address.country_code,
        "state": shipping_address.state_name,
        "zipCode": shipping_address.zip_code
    }

def canonical_profile_to_valor(profile: Profile, profile_id: str) -> dict:

    valor_card = emit_valor_card(profile.card)
    valor_shipping = emit_valor_shipping(profile.shipping_address)
    valor_billing = valor_shipping if profile.billing_same_as_ship else emit_valor_shipping(profile.billing_address)

    return {
        "name": profile.profile_name,
        "email": profile.email,
        "phoneNumber": profile.phone_number,

        "personalCustomsCode":"",
		"pinCode":"",
		"idNumber":"",
		"birthday":"",

        "billingSameAsShipping": profile.billing_same_as_ship,
        "oneCheckout": profile.one_checkout,
        "quickTask": False,
        
        "card": valor_card,
        "shipping": valor_shipping,
        "billing": valor_billing,

        "id": profile_id,
        "totalSpent": "0"
    }

def canonical_profiles_to_valor(profiles: list[Profile]) -> dict:
    valor_profiles = {}

    for profile in profiles:
        profile_id = str(uuid.uuid4())
        valor_profiles[profile_id] = canonical_profile_to_valor(profile, profile_id)

    return valor_profiles