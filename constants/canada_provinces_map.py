"""
Canadian province and territory mappings.

This module defines mappings between Canadian province/territory
full names and their standard postal abbreviations.

Canonical representation:
- Provinces and territories are stored using their
  two-letter Canada Post codes (e.g. "BC", "ON").

Usage:
- Forward mapping (name → code) is used when parsing bot exports
  that provide province names (e.g. "British Columbia").
- Reverse mapping (code → name) is used when emitting profiles
  to bots that require full province names in dropdown fields.

Assumptions:
- Bot profile exports use controlled dropdown values, so input
  province names are assumed to be valid and consistently formatted.
- Strict validation is preferred over normalization.
"""

CANADA_PROVINCE_NAME_TO_CODE_MAP = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",

    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "Yukon": "YT",
}

# Reverse map: ISO code -> full name
CANADA_PROVINCE_CODE_TO_NAME_MAP = {
    code: name for name, code in CANADA_PROVINCE_NAME_TO_CODE_MAP.items()
}

# Set of valid ISO country codes
CANADA_PROVINCE_CODE_SET = set(CANADA_PROVINCE_NAME_TO_CODE_MAP.values())