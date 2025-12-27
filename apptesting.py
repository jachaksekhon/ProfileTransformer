import json
from dataclasses import asdict

from parsers.valor_parser import map_valor_to_canonical
from emitters.stellar_emitter import canonical_profiles_to_stellar
from parsers.stellar_parser import map_stellar_to_canonical
from emitters.valor_emitter import canonical_profiles_to_valor

from parsers.cybersole_parser import map_cybersole_to_canonical
from dataclasses import asdict



def test_valor_to_canonical_to_stellar():
    """
    End-to-end test:
    Valor JSON -> Canonical -> Stellar JSON
    """

    # 1. Load Valor input
    with open("valorprofiles.json", "r", encoding="utf-8") as f:
        valor_profiles = json.load(f)

    print(f"Loaded {len(valor_profiles)} Valor profiles")

    # 2. Valor -> Canonical
    canonical_profiles = map_valor_to_canonical(valor_profiles)

    print(f"Converted to {len(canonical_profiles)} canonical profiles")

    # Optional: sanity check first profile
    if canonical_profiles:
        print("\nSample canonical profile:")
        print(canonical_profiles[0])

    # 3. Canonical -> Stellar
    stellar_profiles = canonical_profiles_to_stellar(canonical_profiles)

    print(f"\nGenerated {len(stellar_profiles)} Stellar profiles")

    # 4. Write Stellar output to file
    with open("stellar_output.json", "w", encoding="utf-8") as f:
        json.dump(stellar_profiles, f, indent=2)

    print("\nWrote Stellar output to stellar_output.json")

def test_stellar_to_canonical_to_valor():
    """
    End-to-end test:
    Stellar JSON -> Canonical -> Valor JSON
    """

    # 1. Load Valor input
    with open("stellarprofiles.json", "r", encoding="utf-8") as f:
        stellar_profiles = json.load(f)

    print(f"Loaded {len(stellar_profiles)} stellar profiles")

    # 2. Valor -> Canonical
    canonical_profiles = map_stellar_to_canonical(stellar_profiles)

    print(f"Converted to {len(canonical_profiles)} canonical profiles")

    # Optional: sanity check first profile
    if canonical_profiles:
        print("\nSample canonical profile:")
        print(canonical_profiles[0])

    # 3. Canonical -> Stellar
    valor_profiles = canonical_profiles_to_valor(canonical_profiles)

    print(f"\nGenerated {len(stellar_profiles)} Stellar profiles")

    # 4. Write Stellar output to file
    with open("valor_output.txt", "w", encoding="utf-8") as f:
        json.dump(valor_profiles, f, indent=2)

    print("\nWrote Valor output to valor_output.json")

def test_cyber_to_canonical():
    """
    End-to-end test:
    cyber JSON -> Canonical 
    """

    # 1. Load Valor input
    with open("cyberprofiles.json", "r", encoding="utf-8") as f:
        cyber_profiles = json.load(f)

    print(f"Loaded {len(cyber_profiles)} cyber profiles")

    # 2. Valor -> Canonical
    canonical_profiles = map_cybersole_to_canonical(cyber_profiles)

    print(f"Converted to {len(canonical_profiles)} canonical profiles")

    # # Optional: sanity check first profile
    # if canonical_profiles:
    #     print("\nSample canonical profile:")
    #     print(canonical_profiles[0])

    # # 3. Canonical -> Stellar
    # valor_profiles = canonical_profiles_to_valor(canonical_profiles)

    # print(f"\nGenerated {len(stellar_profiles)} Stellar profiles")

    # 4. Write Stellar output to file
    with open("cyber_canonical.json", "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in canonical_profiles], f, indent=2)


    print("\nWrote canonical output to cyber_canonical.json")

if __name__ == "__main__":
    # test_valor_to_canonical_to_stellar()
    # test_stellar_to_canonical_to_valor()
    test_cyber_to_canonical()
