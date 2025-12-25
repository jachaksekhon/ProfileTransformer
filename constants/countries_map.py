"""
Mapping of countries with their two letter country codes

Canonical representation:
- country is stored as ISO alpha-2 code (e.g. 'CA', 'US')

Bots may require:
- Country code
- Or full country name
"""

COUNTRY_NAME_TO_CODE_MAP = {
    "Canada": "CA",
    "United States": "US",
    "Mexico": "MX",

    "United Kingdom": "GB",
    "Ireland": "IE",

    "France": "FR",
    "Germany": "DE",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",

    "Japan": "JP",
    "South Korea": "KR",
    "China": "CN",
    "Hong Kong": "HK",
    "Taiwan": "TW",

    "Australia": "AU",
    "New Zealand": "NZ",
}

# Reverse map: ISO code -> full name
COUNTRY_CODE_TO_NAME_MAP = {
    code: name for name, code in COUNTRY_NAME_TO_CODE_MAP.items()
}

# Set of valid ISO country codes
COUNTRY_CODE_SET = set(COUNTRY_CODE_TO_NAME_MAP.keys())

def find_country_from_code(country_code: str) -> str:
    """
    Resolve a country name from an ISO alpha-2 country code.

    Raises:
        ValueError: if the country code is unsupported.
    """

    if country_code in COUNTRY_CODE_SET:
        return COUNTRY_CODE_TO_NAME_MAP[country_code]
    
    raise ValueError(f"Unsupported country code: {country_code}")
