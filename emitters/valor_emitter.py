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

from models.canonical import Profile, Address, Card