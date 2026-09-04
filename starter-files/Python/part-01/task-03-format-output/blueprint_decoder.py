import re

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
    print("\n" + separator)
    print("🔐 DECODED SECRETS REPORT".center(50))
    print(separator)
    print(f"Total secrets found: {len(secrets)}\n")
    
    # Let Copilot suggest: format each secret with index
    # Consider: padding, alignment, special characters
    for index, secret in enumerate(secrets, 1):
        print(f"  [{index:2d}] {secret}")

    
    print("\n" + separator + "\n")

# Function to categorize a single secret by type splitting on : and reporting others as uncategorised
def categorize_secret(secret):
    """Return the category for a single secret string."""
    if ":" in secret:
        return secret.split(":", 1)[0].strip()
    return "UNCLASSIFIED"



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
