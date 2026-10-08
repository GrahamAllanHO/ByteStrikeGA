"""Integration tests with mock HTTP server."""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import pytest

from decoder import DecodeError, decode

# Sample blueprint data for testing
SAMPLE_BLUEPRINT = """
League Blueprint Archive - Project Cipher
========================================
Classification: Top Secret
Date: 2026-02-15

Mission Overview: {* SECURE_COMMS_PROTOCOL *}

Technical Specifications:
- Standard encryption layer (public)
- Quantum-resistant algorithm framework
- Multi-factor authentication required

Hidden Intel Fragment 1: {* AGENT_CODENAME: SHADOWMIND *}

Infrastructure Notes:
The system uses distributed nodes across 47 locations.
Primary data center coordinates are classified.
Backup systems engage automatically during network disruption.

Critical Security Note: {* VAULT_ACCESS_CODE: DELTA-7-7-ECHO *}

Deployment Information: {* MEETING_LOCATION: SAFEHOUSE_BERLIN_CHECKPOINT_C *}

Emergency Contact: {* EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE *}
"""


class MockBlueprintHandler(BaseHTTPRequestHandler):
    """HTTP request handler that serves sample blueprint data."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/blueprint":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(SAMPLE_BLUEPRINT.encode("utf-8"))
        elif self.path == "/empty":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"No secrets here")
        elif self.path == "/error":
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress HTTP server logging."""
        pass


@pytest.fixture
def mock_server():
    """Start a mock HTTP server in a background thread."""
    server = HTTPServer(("127.0.0.1", 0), MockBlueprintHandler)
    host, port = server.server_address

    # Run server in background thread
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.daemon = True
    thread.start()

    # Give server time to start
    time.sleep(0.1)

    yield f"http://{host}:{port}"

    # Cleanup
    server.shutdown()
    server.server_close()


@pytest.fixture
def blueprint_url(mock_server):
    """URL to mock blueprint endpoint."""
    return f"{mock_server}/blueprint"


@pytest.fixture
def empty_url(mock_server):
    """URL to empty endpoint."""
    return f"{mock_server}/empty"


@pytest.fixture
def error_url(mock_server):
    """URL to error endpoint."""
    return f"{mock_server}/error"


class TestMockServerIntegration:
    """Integration tests using mock server."""

    def test_mock_server_serves_blueprint(self, blueprint_url):
        """Test that mock server returns blueprint data correctly."""
        # Use custom opener to bypass URL validation for localhost
        import urllib.request

        with urllib.request.urlopen(blueprint_url, timeout=5) as resp:
            text = resp.read().decode("utf-8")
        assert "SECURE_COMMS_PROTOCOL" in text
        assert "SHADOWMIND" in text

    def test_decode_from_memory(self):
        """Test decoding blueprint data from memory directly."""
        from decoder import extract_between

        result = extract_between(SAMPLE_BLUEPRINT, "{*", "*}")
        secrets = result.split("\n")
        assert len(secrets) == 5
        assert "SECURE_COMMS_PROTOCOL" in secrets[0]

    def test_fetch_and_decode_with_mock(self, monkeypatch):
        """Test full fetch-decode pipeline with mocked fetch."""
        monkeypatch.setattr("decoder.fetch_text", lambda *a, **k: SAMPLE_BLUEPRINT)
        result = decode("http://example.com/blueprint", "{*", "*}", retries=1)
        secrets = result.split("\n")
        assert len(secrets) == 5
        assert "SECURE_COMMS_PROTOCOL" in secrets[0]
        assert "SHADOWMIND" in secrets[1]
        assert "DELTA-7-7-ECHO" in secrets[2]

    def test_extract_all_secrets_from_sample(self):
        """Test extracting all secrets from sample blueprint."""
        from decoder import extract_between

        result = extract_between(SAMPLE_BLUEPRINT, "{*", "*}")
        secrets = result.split("\n")
        assert len(secrets) == 5

    def test_extract_partial_content(self):
        """Test extracting specific section without secret markers."""
        from decoder import extract_between

        result = extract_between(SAMPLE_BLUEPRINT, "Mission Overview:", "Technical")
        assert "SECURE_COMMS_PROTOCOL" in result

    def test_mock_server_empty_endpoint(self, empty_url):
        """Test mock server empty endpoint."""
        import urllib.request

        with urllib.request.urlopen(empty_url, timeout=5) as resp:
            text = resp.read().decode("utf-8")
        assert text == "No secrets here"

    def test_decode_empty_response_error(self, monkeypatch):
        """Test error when response has no secrets."""
        monkeypatch.setattr("decoder.fetch_text", lambda *a, **k: "No secrets here")
        with pytest.raises(DecodeError, match="No content found between"):
            decode("http://example.com/empty", "{*", "*}", retries=1)

    def test_mock_server_error_endpoint(self, error_url):
        """Test mock server error endpoint returns 500."""
        import urllib.request

        with pytest.raises(urllib.request.HTTPError) as exc_info:
            urllib.request.urlopen(error_url, timeout=5)
        assert exc_info.value.code == 500

    def test_blueprint_has_expected_secrets(self):
        """Test that sample blueprint contains expected secrets."""
        secrets_to_find = [
            "SECURE_COMMS_PROTOCOL",
            "SHADOWMIND",
            "DELTA-7-7-ECHO",
            "SAFEHOUSE_BERLIN_CHECKPOINT_C",
            "NIGHTFALL_SEQUENCE_ACTIVE",
        ]
        for secret in secrets_to_find:
            assert secret in SAMPLE_BLUEPRINT
