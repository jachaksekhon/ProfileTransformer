from dataclasses import dataclass

# Middle ground object created to allow addition bot extensions to be included if needed

@dataclass
class Address:
    """ 
    Canonical address model.

    Invariants:
    - address_line_2 can be null
    - state/province is 2 letters (e.g "BC")
    """
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: str
    country_name: str
    country_code: str
    state_name: str
    state_code: str
    city: str
    zip_code: str

@dataclass
class Card:
    """ 
    Canonical card model.

    Invariants:
    - card_type stored as all lower case (e.g "amex", "visa")
    - number stored as one contiguous string (e.g "123456789...")
    """
    holder: str
    card_type: str
    number: str
    exp_month: str
    exp_year: str
    cvv: str

@dataclass
class Profile:
    """ 
    Canonical profile model.

    Invariants:
    - phone_number stored as one contiguous string (e.g 6041230123)
    """
    profile_name: str
    email: str
    phone_number: str

    shipping_address: Address
    billing_address: Address
    billing_same_as_ship: bool

    card: Card

    one_checkout: bool
