import re
from pathlib import Path

RESET = "\033[0m"
HEADER_COLOR = "\033[96m"
TITLE_COLOR = "\033[95m"
SECRET_COLORS = [
    "\033[91m",
    "\033[92m",
    "\033[93m",
    "\033[94m",
    "\033[95m",
    "\033[96m",
]


def find_blueprint_data():
    current = Path(__file__).resolve()

    for parent in current.parents:
        candidate = parent / "blueprint-data.txt"
        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find blueprint-data.txt")


def extract_secrets(blueprint_text):
    pattern = r'\{\*\s*(.*?)\s*\*\}'
    return re.findall(pattern, blueprint_text)


def secret_label(secret):
    return secret.split(":", 1)[0].strip()


def print_secret_report(blueprint_path, secrets):
    print(f"{HEADER_COLOR}=== Blueprint Secret Decoder ==={RESET}")
    print(f"{TITLE_COLOR}Source:{RESET} {blueprint_path}")
    print(f"{TITLE_COLOR}Secrets Found:{RESET} {len(secrets)}")
    print()

    if not secrets:
        print("No secrets found.")
        return

    color_by_label = {}

    for index, secret in enumerate(secrets, start=1):
        label = secret_label(secret)
        if label not in color_by_label:
            color_by_label[label] = SECRET_COLORS[len(color_by_label) % len(SECRET_COLORS)]
        color = color_by_label[label]
        print(f"{color}{index}. {secret}{RESET}")


def main():
    blueprint_path = find_blueprint_data()
    blueprint_text = blueprint_path.read_text(encoding="utf-8")
    secrets = extract_secrets(blueprint_text)
    print_secret_report(blueprint_path, secrets)


if __name__ == "__main__":
    main()
