CANADA_PROVINCE_MAP = {
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

CANADA_PROVINCE_CODE_SET = set(CANADA_PROVINCE_MAP.values())

CANADA_PROVINCE_REVERSE_MAP = {
    code: name for name, code in CANADA_PROVINCE_MAP.items()
}