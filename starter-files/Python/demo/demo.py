"""Extract and display secrets embedded in a blueprint file."""

import re
import sys
from pathlib import Path

ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def ansi_rgb(red, green, blue):
    """Build an ANSI 24-bit foreground color escape sequence.

    Args:
        red: Red channel value.
        green: Green channel value.
        blue: Blue channel value.

    Returns:
        The ANSI escape sequence for the specified color.
    """
    return f"\033[38;2;{red};{green};{blue}m"


ANSI_COLORS = (
    ansi_rgb(231, 76, 60),   # Crimson
    ansi_rgb(46, 204, 113),  # Emerald
    ansi_rgb(241, 196, 15),  # Sunflower
    ansi_rgb(52, 152, 219),  # River
    ansi_rgb(155, 89, 182),  # Amethyst
    ansi_rgb(26, 188, 156),  # Turquoise
)
# Function to read a blueprint file and extract all secrets marked between {* and *}
# Example: League Blueprint contains {* AGENT_CODENAME: SHADOWMIND *}
# Should extract: "AGENT_CODENAME: SHADOWMIND" (without the markers)
# Uses regex pattern to find all occurrences
# Returns a list of extracted secrets
def extract_secrets_from_blueprint(file_path):
    """Extract text enclosed by ``{*`` and ``*}`` from a blueprint.

    Args:
        file_path: Path to the blueprint file.

    Returns:
        A list of extracted secret strings without their marker delimiters.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    pattern = r'\{\*\s*(.*?)\s*\*\}'
    return re.findall(pattern, content)


def find_default_blueprint():
    """Find ``blueprint-data.txt`` in this file's parent directories.

    Returns:
        The path to the first matching blueprint file.

    Raises:
        FileNotFoundError: If no matching blueprint file is found.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "blueprint-data.txt"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not find blueprint-data.txt")


def split_secret(secret):
    """Separate a secret into its label and value.

    A secret without a colon is returned as a label with an empty value.

    Args:
        secret: Secret text, optionally formatted as ``label: value``.

    Returns:
        A pair containing the stripped label and value.
    """
    if ":" not in secret:
        return secret.strip(), ""
    label, value = secret.split(":", 1)
    return label.strip(), value.strip()


def tab_padding(label, target_column=24, tab_width=8):
    """Calculate tabs that align a value after a label.

    Args:
        label: The label preceding the value.
        target_column: Desired starting column for the value.
        tab_width: Number of columns represented by one tab.

    Returns:
        A string containing the required tab characters.

    Examples:
        >>> tab_padding("NAME")
        '\t\t\t'
        >>> tab_padding("LONG_LABEL", target_column=16)
        '\t'
    """
    visible_width = len(label) + 1
    tabs_needed = max(1, (target_column - visible_width + tab_width - 1) // tab_width)
    return "\t" * tabs_needed


def format_secret(secret, label_colors):
    """Format a secret with a consistent ANSI color for its label.

    Args:
        secret: Secret text, optionally containing a colon-separated value.
        label_colors: Mapping from labels to their assigned ANSI colors; new
            labels are added to this mapping.

    Returns:
        The formatted secret string.
    """
    label, value = split_secret(secret)

    if label not in label_colors:
        label_colors[label] = ANSI_COLORS[len(label_colors) % len(ANSI_COLORS)]

    color = label_colors[label]
    if value:
        return f"{color}{ANSI_BOLD}{label}:{ANSI_RESET}{tab_padding(label)}{value}"
    return f"{color}{ANSI_BOLD}{label}{ANSI_RESET}"


def main():
    """Load a blueprint and print its extracted secrets."""
    blueprint_path = Path(sys.argv[1]) if len(sys.argv) > 1 else find_default_blueprint()
    secrets = extract_secrets_from_blueprint(blueprint_path)

    if secrets:
        print(f"{ANSI_BOLD}LABEL\t\tVALUE{ANSI_RESET}")
        print("-----\t\t-----")
        label_colors = {}
        for secret in secrets:
            print(format_secret(secret, label_colors))
    else:
        print("No secrets found.")


if __name__ == "__main__":
    main()
