"""
Mapping of countries with their two letter country codes

Canonical representation:
- country is stored as ISO alpha-2 code (e.g. 'CA', 'US')

Bots may require:
- Country code
- Or full country name
"""

import constants.canada_provinces as provinces_helper
import constants.us_states as states_helper

COUNTRY_NAME_TO_CODE_MAP = {
    "Canada": "CA",
    "United States": "US",
    # "Mexico": "MX",

    # "United Kingdom": "GB",
    # "Ireland": "IE",

    # "France": "FR",
    # "Germany": "DE",
    # "Italy": "IT",
    # "Spain": "ES",
    # "Netherlands": "NL",

    # "Japan": "JP",
    # "South Korea": "KR",
    # "China": "CN",
    # "Hong Kong": "HK",
    # "Taiwan": "TW",

    # "Australia": "AU",
    # "New Zealand": "NZ",
}

# Reverse map: ISO code -> full name
COUNTRY_CODE_TO_NAME_MAP = {
    code: name for name, code in COUNTRY_NAME_TO_CODE_MAP.items()
}

# Set of valid ISO country codes
COUNTRY_CODE_SET = set(COUNTRY_NAME_TO_CODE_MAP.values())

COUNTRY_NAME_SET = set(COUNTRY_NAME_TO_CODE_MAP.keys())

def find_country_from_code(country_code: str) -> str:
    """
    Resolve a country name from an ISO alpha-2 country code.

    Raises:
        ValueError: if the country code is unsupported.
    """

    if country_code in COUNTRY_CODE_SET:
        return COUNTRY_CODE_TO_NAME_MAP[country_code]
    
    raise ValueError(f"Unsupported country code: {country_code}")

def find_code_from_country(country_name: str) -> str:
    """
    Resolve a country code from a country name.

    Raises:
        ValueError: if the country name is unsupported.
    """

    if country_name in COUNTRY_NAME_SET:
        return COUNTRY_NAME_TO_CODE_MAP[country_name]
    
    raise ValueError(f"Unsupported country name: {country_name}")


def province_or_state_code_finder(country_code: str, state_or_province_name: str) -> str:
      """
      Returns the province or state code given province name or state name.

      E.g: "BC" for British Columbia or "TX" for Texas
      """
      if country_code == "CA":
            return provinces_helper.find_province_from_code(state_or_province_name)
      elif country_code == "US":
            return states_helper.find_state_from_code(state_or_province_name)
      else:
            raise ValueError(
                  f"Country '{country_code}' is not supported yet"
            )

