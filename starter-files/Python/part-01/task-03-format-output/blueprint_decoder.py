import re

COLOR_PALETTE = [
    "\033[91m",  # Bright red
    "\033[92m",  # Bright green
    "\033[93m",  # Bright yellow
    "\033[94m",  # Bright blue
    "\033[95m",  # Bright magenta
    "\033[96m",  # Bright cyan
    "\033[31m",  # Red
    "\033[32m",  # Green
    "\033[33m",  # Yellow
    "\033[34m",  # Blue
]
BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def decode_blueprint(filename):
    with open(filename, "r") as file:
        content = file.read()

    pattern = r"\{\* (.*?) \*\}"
    secrets = re.findall(pattern, content)
    return secrets


# Function to format and display secrets in a professional report
# Includes header, separator lines, numbered list, and footer
def display_secrets_report(secrets):
    """Display extracted secrets in a formatted report.

    Args:
        secrets (list): List of secret strings to display
    """
    separator = "=" * 50
    category_colors = {}

    print("\n" + separator)
    print("🔐 DECODED SECRETS REPORT".center(50))
    print(separator)
    print(f"Total secrets found: {len(secrets)}\n")

    for index, secret in enumerate(secrets, 1):
        category, display_text = categorize_secret(secret)
        if category not in category_colors:
            color_index = len(category_colors) % len(COLOR_PALETTE)
            category_colors[category] = COLOR_PALETTE[color_index]

        color = category_colors[category]
        print(f"{color}  [{index:2d}] [{category}] {BOLD}{display_text}{COLOR_RESET}")

    print("\n" + separator + "\n")


# Function to categorize a single secret by type splitting on : and reporting others as uncategorised
def categorize_secret(secret):
    """Return the category and display value for a single secret string."""
    if ":" in secret:
        category, secret_value = secret.split(":", 1)
        return category.strip(), secret_value.strip()
    return "UNCLASSIFIED", secret


# Enhanced version with error handling
# If file doesn't exist, return an empty list and print an error message
def decode_blueprint_safe(filename):
    try:
        return decode_blueprint(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []


if __name__ == "__main__":
    # Test error handling
    secrets = decode_blueprint_safe("nonexistent.txt")
    print(f"Found {len(secrets)} secrets")

    # Test normal operation
    secrets = decode_blueprint_safe("blueprint-data.txt")
    print(f"Found {len(secrets)} secrets")
    display_secrets_report(secrets)
