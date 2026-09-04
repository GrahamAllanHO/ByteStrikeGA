import re
# Function to read a blueprint file and extract all secrets marked between {* and *}
# Example: League Blueprint contains {* AGENT_CODENAME: SHADOWMIND *}
# Should extract: "AGENT_CODENAME: SHADOWMIND" (without the markers)
# Uses regex pattern to find all occurrences
# Returns a list of extracted secrets

def extract_secrets_from_blueprint(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    pattern = r'\{\*\s*(.*?)\s*\*\}'
    secrets = re.findall(pattern, content)
    return secrets      

# Example usage:
# secrets = extract_secrets_from_blueprint('path/to/blueprint.txt')
# print(secrets)    

#Test the decoder
if __name__ == "__main__":
    secrets = extract_secrets_from_blueprint("blueprint-data.txt")
    print("Extracted secrets:")
    for secret in secrets:
        print(secret)
