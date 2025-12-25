"""
U.S. state mappings.

Canonical representation:
- States are stored using USPS two-letter codes (e.g. "CA", "NY").

Usage:
- Name → code mapping is used when parsing bot exports
  that provide full state names.
- Code → name mapping is used when emitting profiles
  to bots that require full state names.
"""

US_STATE_NAME_TO_CODE_MAP = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


# Reverse map: ISO code -> full name
US_STATE_CODE_TO_NAME_MAP = {
    code: name for name, code in US_STATE_NAME_TO_CODE_MAP.items()
}

# Set of valid ISO country codes
US_STATE_CODE_SET = set(US_STATE_NAME_TO_CODE_MAP.values())

# Set of valid country names
US_STATE_NAME_SET = set(US_STATE_NAME_TO_CODE_MAP.keys())

def find_state_from_code(state_code: str) -> str:
    """
    Resolve a province name from an ISO alpha-2 state code.

    Raises:
        ValueError: if the state code is unsupported.
    """
    if state_code in US_STATE_CODE_SET:
        return US_STATE_CODE_TO_NAME_MAP[state_code]
    
    raise ValueError(f"Unsupported state code: {state_code}")

def find_code_from_state(state_name: str) -> str:
    """
    Resolve a state code from a state name.

    Raises:
        ValueError: if the state name is unsupported.
    """
    if state_name in US_STATE_NAME_SET:
        return US_STATE_NAME_TO_CODE_MAP[state_name]
    
    raise ValueError(f"Unsupported state name: {state_name}")