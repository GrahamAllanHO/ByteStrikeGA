import re
from typing import Dict, List
import pytest


def read_blueprint(filename: str) -> str:
    """Read and return the contents of a blueprint file.

    Args:
        filename: Path to the file to read.

    Returns:
        The complete file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be opened or read.

    Example:
        >>> read_blueprint("blueprint-data.txt")
        'API_KEY: example-secret\n'
    """
    with open(filename, "r") as f:
        return f.read()


def extract_secrets(content: str) -> List[str]:
    """Extract all secret-like lines from blueprint content.

    Identifies lines that match the pattern PREFIX: value, where PREFIX is
    uppercase letters followed by a colon and at least one non-whitespace
    character. This is useful for finding credential entries in blueprints.

    Args:
        content: The blueprint content as a string, potentially containing
                 multiple lines with secret-like entries.

    Returns:
        A list of strings, each representing a complete secret line found
        in the content. If no matches are found, returns an empty list.

    Raises:
        None

    Example:
        >>> extract_secrets("AWS: aws-key-123\\nDB: db-password-456")
        ['AWS: aws-key-123', 'DB: db-password-456']

        >>> extract_secrets("This has no secrets")
        []
    """
    pattern = r"^[A-Z]+:\s*\S+.*$"
    return re.findall(pattern, content, re.MULTILINE)


def categorize_secrets(secrets: List[str]) -> Dict[str, List[str]]:
    """Organize secrets into categories by their prefix.

    Parses secrets in the format "PREFIX: value" and groups them by their
    prefix category. Secrets without a colon are placed in the "uncategorized"
    category. Multiple secrets with the same prefix are collected into a list
    under that prefix key.

    Args:
        secrets: A list of secret strings, each ideally formatted as
                "PREFIX: value". Strings without a colon are treated as
                uncategorized values.

    Returns:
        A dictionary where keys are prefix categories (strings) and values
        are lists of secret values associated with that category. Example:
        {"AWS": ["aws-key-123", "aws-key-789"], "DB": ["db-password-456"]}

    Raises:
        None

    Example:
        >>> categorize_secrets(["AWS: aws-key-123", "DB: db-password-456"])
        {'AWS': ['aws-key-123'], 'DB': ['db-password-456']}

        >>> categorize_secrets(["unclassified-secret"])
        {'uncategorized': ['unclassified-secret']}
    """
    cats: Dict[str, List[str]] = {}
    for s in secrets:
        if ":" in s:
            key, value = s.split(":", 1)
            key = key.strip()
            value = value.strip()
        else:
            key = "uncategorized"
            value = s.strip()
        if key not in cats:
            cats[key] = []
        cats[key].append(value)
    return cats


def decode_blueprint_safe(filename: str) -> Dict[str, List[str]]:
    """Safely read a blueprint file and extract and categorize secrets.

    Attempts to read a blueprint file and extract all secret-like entries
    in the format PREFIX: value. Handles file not found errors gracefully
    and prints a detailed report of discovered secrets to stdout. This is
    the safe wrapper around the extraction and categorization pipeline.

    Args:
        filename: Path to the blueprint file to decode.

    Returns:
        A dictionary of categorized secrets with categories as keys and lists
        of values as values. Returns an empty dict if the file cannot be read.

    Raises:
        None (exceptions are caught and handled internally; errors are
        reported via print statements)

    Example:
        >>> result = decode_blueprint_safe("blueprint.txt")
        # Output to stdout:
        # ========================================
        # DECODED SECRETS REPORT
        # ========================================
        # Found 2 secret(s):
        #
        # 1. AWS: aws-key-123
        # 2. DB: db-password-456
        # ========================================
        >>> result
        {'AWS': ['aws-key-123'], 'DB': ['db-password-456']}

        >>> result = decode_blueprint_safe("nonexistent.txt")
        # Output to stdout:
        # Error: 'nonexistent.txt' not found.
        >>> result
        {}
    """
    try:
        content = read_blueprint(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return {}
    secrets = extract_secrets(content)
    print("=" * 40)
    print("DECODED SECRETS REPORT")
    print("=" * 40)
    print(f"Found {len(secrets)} secret(s):\n")
    for i, s in enumerate(secrets, 1):
        print(f"{i}. {s}")
    print("=" * 40)
    return categorize_secrets(secrets)


decode_blueprint = decode_blueprint_safe