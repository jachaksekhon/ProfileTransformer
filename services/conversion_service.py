import json
import os
from registries.bot_registry import PARSERS, EMITTERS


def load_config():
    """
    Load conversion configuration from config.json if it exists.
    Returns a dict or None.
    """
    if not os.path.exists("config.json"):
        return None

    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_source_target(cli_source: str | None, cli_target: str | None):
    """
    Resolve source/target from CLI args or config.json.
    CLI args take precedence.
    """
    if cli_source and cli_target:
        return cli_source, cli_target

    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        source = config.get("from")
        target = config.get("to")

        if not source or not target:
            raise ValueError(
                "config.json must contain both 'from' and 'to' fields."
            )

        return source, target

    raise RuntimeError(
        "No conversion source/target specified.\n"
        "Use CLI arguments or create config.json."
    )

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
