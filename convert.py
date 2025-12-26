import argparse
from services.conversion_service import convert
from registries.bot_registry import (
    SUPPORTED_SOURCE_BOTS,
    SUPPORTED_TARGET_BOTS
)


def main():
    parser = argparse.ArgumentParser(
        description="Convert bot profiles between Stellar and Valor"
    )

    parser.add_argument(
        "--from",
        dest="source",
        choices=SUPPORTED_SOURCE_BOTS,
        required=True,
        help="Source bot type"
    )

    parser.add_argument(
        "--to",
        dest="target",
        choices=SUPPORTED_TARGET_BOTS,
        required=True,
        help="Target bot type"
    )

    args = parser.parse_args()

    try:
        count = convert(args.source, args.target)
        print(f"Successfully converted {count} profiles")
    except Exception as e:
        print(f"Conversion failed: {e}")
        raise


if __name__ == "__main__":
    main()
