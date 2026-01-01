import argparse
from services.conversion_service import convert, resolve_source_target
from registries.bot_registry import (
    SUPPORTED_SOURCE_BOTS,
    SUPPORTED_TARGET_BOTS
)


def main():
    parser = argparse.ArgumentParser(
        description="Convert your bot profiles!"
    )

    parser.add_argument(
        "--from",
        dest="source",
        choices=SUPPORTED_SOURCE_BOTS,
        required=False,
        help="Source bot type"
    )

    parser.add_argument(
        "--to",
        dest="target",
        choices=SUPPORTED_TARGET_BOTS,
        required=False,
        help="Target bot type"
    )

    args = parser.parse_args()

    try:
        source, target = resolve_source_target(args.source, args.target)

        count = convert(source, target)
        print(f"Successfully converted {count} profiles")

    except Exception as e:
        print(f"Conversion failed: {e}")
        input("\nPress Enter to exit...")  # helpful for double-click users


if __name__ == "__main__":
    main()
