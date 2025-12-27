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