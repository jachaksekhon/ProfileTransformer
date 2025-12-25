def require_key(data: dict, key: str, context: str):
    """
    Retrieve a required key from a dictionary or raise a descriptive error.
    Ensures passed in JSON matches for any future updates made to export/import
    behaviors from bots

    Args:
        data: The source dictionary.
        key: The required key name.
        context: Human-readable context for error messages.

    Raises:
        ValueError: If the key is missing.

    Returns:
        The value associated with the key.
    """
    try:
        return data[key]
    except KeyError:
        raise ValueError(
            f"Missing required field '{key}' in {context}. "
            f"Available keys: {list(data.keys())}"
        )
