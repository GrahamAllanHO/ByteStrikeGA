from blueprint_decoder import categorize_secrets, extract_secrets


def test_extract_secrets_happy_path():
	blueprint = "AWS: aws-key-123"

	assert extract_secrets(blueprint) == ["AWS: aws-key-123"]


def test_extract_secrets_returns_empty_list_when_there_are_no_matches():
	assert extract_secrets("This blueprint contains no secrets.") == []

1
def test_extract_secrets_finds_multiple_secrets():
	blueprint = "AWS: aws-key-123\nDB: db-password-456"

	assert extract_secrets(blueprint) == [
		"AWS: aws-key-123",
		"DB: db-password-456",
	]


def test_categorize_secrets_groups_values_by_prefix():
	secrets = ["AWS: aws-key-123", "DB: db-password-456", "AWS: aws-key-789"]

	assert categorize_secrets(secrets) == {
		"AWS": ["aws-key-123", "aws-key-789"],
		"DB": ["db-password-456"],
	}


def test_categorize_secrets_handles_values_without_a_colon():
	assert categorize_secrets(["unclassified-secret"]) == {
		"uncategorized": ["unclassified-secret"]
	}
