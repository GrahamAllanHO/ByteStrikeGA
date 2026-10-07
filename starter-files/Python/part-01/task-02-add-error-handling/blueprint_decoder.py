import re

# Function to read a blueprint file and extract all secrets marked between {* and *}
# Example: League Blueprint contains {* AGENT_CODENAME: SHADOWMIND *}
# Should extract: "AGENT_CODENAME: SHADOWMIND" (without the markers)
# Uses regex pattern to find all occurrences
# Returns a list of extracted secrets
def decode_blueprint(filename):
    with open(filename, "r") as file:
        content = file.read()

    # Use regex to find all secrets between {* and *}
    pattern = r"\{\* (.*?) \*\}"
    secrets = re.findall(pattern, content)
    return secrets


# Enhanced version with error handling
# If file doesn't exist, return an empty list and print an error message
def decode_blueprint_safe(filename):
    # TODO: Add try-except to catch FileNotFoundError
    # TODO: If file doesn't exist, print error and return empty list
    # TODO: Otherwise, call decode_blueprint and return the secrets
    
    # Validate filename is not empty or None
    if not filename or not isinstance(filename, str):
        print(f"Error: Invalid filename. Must be a non-empty string.")
        return []
    
    try:
        return decode_blueprint(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IsADirectoryError:
        print(f"Error: '{filename}' is a directory, not a file.")
        return []
    except PermissionError:
        print(f"Error: Permission denied reading file '{filename}'.")
        return []
    except UnicodeDecodeError:
        print(f"Error: Unable to read file '{filename}' - encoding issue.")
        return []
    except Exception as e:
        print(f"Error: Unexpected error reading file '{filename}': {type(e).__name__}")
        return []


if __name__ == "__main__":
    # Test error handling
    secrets = decode_blueprint_safe("nonexistent.txt")
    print(f"Found {len(secrets)} secrets")

    # Test normal operation
    secrets = decode_blueprint_safe("blueprint-data.txt")
    print(f"Found {len(secrets)} secrets")
