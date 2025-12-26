import json
from registries.bot_registry import PARSERS, EMITTERS


def convert(from_bot: str, to_bot: str) -> int:
    """
    Convert profiles from one bot format to another via the canonical model.

    Flow:
        Raw input (bot-specific)
            -> Canonical profiles
            -> Bot-specific output

    Returns:
        int: number of profiles converted
    """

    if from_bot == to_bot:
        raise ValueError("Source and target bots cannot be the same")

    if from_bot not in PARSERS:
        raise ValueError(f"Unsupported source bot: {from_bot}")

    if to_bot not in EMITTERS:
        raise ValueError(f"Unsupported target bot: {to_bot}")
    
    # begin processing file

    parser_cfg = PARSERS[from_bot]
    input_file = parser_cfg["file"]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Input file '{input_file}' not found. "
            f"Please create it before running the conversion."
        )
    
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Input file '{input_file}' contains invalid JSON: {e}"
        )

    # convert to canonical

    canonical_profiles = parser_cfg["parser"](raw_data)

    if not canonical_profiles:
        raise ValueError("No profiles were parsed from input")
    
    # canonical to source

    emitter_cfg = EMITTERS[to_bot]
    output_profiles = emitter_cfg["emitter"](canonical_profiles)

    with open(emitter_cfg["file"], "w", encoding="utf-8") as f:
        json.dump(output_profiles, f, indent=2)

    return len(canonical_profiles)
