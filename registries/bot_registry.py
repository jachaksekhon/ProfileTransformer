"""
Docstring for registries.bot_registry

Holds the supported parsers and emitters this program supports.
"""

from parsers.stellar_parser import stellar_profile_to_canonical
from parsers.valor_parser import map_valor_to_canonical

from emitters.stellar_emitter import canonical_profiles_to_stellar
from emitters.valor_emitter import canonical_profiles_to_valor


PARSERS = {
    "stellar": {
        "file": "stellarprofiles.json",
        "parser": lambda data: [
            stellar_profile_to_canonical(p) for p in data
        ]
    },
    "valor": {
        "file": "valorprofiles.json",
        "parser": map_valor_to_canonical
    }
}

EMITTERS = {
    "stellar": {
        "file": "stellar_output.json",
        "emitter": canonical_profiles_to_stellar
    },
    "valor": {
        "file": "valor_output.txt",
        "emitter": canonical_profiles_to_valor
    }
}

SUPPORTED_SOURCE_BOTS = list(PARSERS.keys())
SUPPORTED_TARGET_BOTS = list(EMITTERS.keys())

