"""Tests for league mission decoder."""

import sys
import urllib.error

import pytest

from decoder import DecodeError, extract_between, fetch_text


def test_extract_between_ok():
    assert extract_between("xx[ hello ]yy", "[", "]") == "hello"


def test_extract_missing_start():
    with pytest.raises(DecodeError):
        extract_between("abc", "[", "]")


def test_extract_missing_end():
    with pytest.raises(DecodeError):
        extract_between("a[bc", "[", "]")


def test_fetch_retries_then_fails():
    calls = []

    def bad(url, timeout):
        calls.append(1)
        raise urllib.error.URLError("boom")

    with pytest.raises(DecodeError):
        fetch_text("http://x", retries=3, backoff=0, opener=bad)
    assert len(calls) == 3


def test_fetch_success():
    class R:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"[ok]"

    assert fetch_text("http://x", opener=lambda u, timeout: R()) == "[ok]"


def test_main_writes_output(tmp_path, monkeypatch):
    from cli import main

    monkeypatch.setattr(
        sys.modules["decoder"], "fetch_text", lambda *a, **k: "A<b>secret</b>"
    )
    out = tmp_path / "o.txt"
    code = main(
        [
            "--source-url",
            "http://x",
            "--marker-start",
            "<b>",
            "--marker-end",
            "</b>",
            "--output",
            str(out),
        ]
    )
    assert code == 0 and out.read_text().strip() == "secret"


# ================================================================ EDGE CASE TESTS
def test_extract_multiple_matches():
    """Test extraction of multiple secrets between markers."""
    text = "Start {* secret1 *} middle {* secret2 *} end {* secret3 *}"
    result = extract_between(text, "{*", "*}")
    assert result == "secret1\nsecret2\nsecret3"


def test_extract_empty_content():
    """Test extraction with empty content between markers."""
    text = "Start {*  *} end"
    result = extract_between(text, "{*", "*}")
    assert result == ""


def test_extract_whitespace_variations():
    """Test extraction with tabs and newlines in markers."""
    text = "Start {*\n  secret\n  *} end"
    result = extract_between(text, "{*", "*}")
    assert result == "secret"


def test_extract_no_matches():
    """Test that error is raised when no matches found."""
    with pytest.raises(DecodeError):
        extract_between("no secrets here", "{*", "*}")


def test_validate_url_ssrf_localhost():
    """Test SSRF protection against localhost."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="not in League source allowlist"):
        validate_url("http://127.0.0.1/page")


def test_validate_url_ssrf_private_ip():
    """Test SSRF protection against private IPs."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="not in League source allowlist"):
        validate_url("http://192.168.1.1/page")


def test_validate_url_invalid_scheme():
    """Test rejection of non-http(s) schemes."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="Only http"):
        validate_url("ftp://example.com/page")


def test_validate_url_file_scheme():
    """Test rejection of file:// scheme."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="Only http"):
        validate_url("file:///etc/passwd")


def test_validate_url_no_hostname():
    """Test rejection of URL without hostname."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="Only http"):
        validate_url("http:///page")


def test_validate_url_not_in_allowlist():
    """Test rejection of hosts not in allowlist."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="not in League source allowlist"):
        validate_url("http://evil.com/page")


def test_validate_url_unresolvable_host():
    """Test handling of unresolvable DNS."""
    from decoder import validate_url

    with pytest.raises(DecodeError, match="not in League source allowlist"):
        validate_url("http://this-domain-definitely-does-not-exist-12345.com/page")


def test_fetch_non_utf8_response():
    """Test handling of non-UTF-8 encoded response."""

    class BadEncoding:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"\xff\xfe"  # Invalid UTF-8

    with pytest.raises(DecodeError, match="Failed to fetch"):
        fetch_text(
            "http://x", retries=1, backoff=0, opener=lambda u, timeout: BadEncoding()
        )


def test_fetch_http_error():
    """Test handling of HTTP errors."""

    def http_error(url, timeout):
        raise urllib.error.HTTPError(url, 500, "Server Error", {}, None)

    with pytest.raises(DecodeError, match="Failed to fetch"):
        fetch_text("http://x", retries=1, backoff=0, opener=http_error)


def test_fetch_timeout_error():
    """Test handling of timeout."""

    def timeout_error(url, timeout):
        raise TimeoutError("Connection timed out")

    with pytest.raises(DecodeError, match="Failed to fetch"):
        fetch_text("http://x", retries=2, backoff=0, opener=timeout_error)


def test_main_missing_required_args():
    """Test CLI with missing required arguments."""
    from cli import main

    with pytest.raises(SystemExit) as exc_info:
        main(["--source-url", "http://x"])
    assert exc_info.value.code == 2  # argparse exits with code 2


def test_main_invalid_retries():
    """Test CLI with invalid retries value."""
    from cli import main

    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--source-url",
                "http://x",
                "--marker-start",
                "a",
                "--marker-end",
                "b",
                "--retries",
                "abc",
            ]
        )
    assert exc_info.value.code == 2  # argparse exits with code 2


def test_main_output_to_readonly_dir(tmp_path, monkeypatch):
    """Test file write error handling."""
    from cli import main
    import os

    ro_dir = tmp_path / "readonly"
    ro_dir.mkdir()
    os.chmod(ro_dir, 0o444)

    monkeypatch.setattr(sys.modules["decoder"], "fetch_text", lambda *a, **k: "secret")
    out_path = ro_dir / "output.txt"

    code = main(
        [
            "--source-url",
            "http://x",
            "--marker-start",
            "a",
            "--marker-end",
            "b",
            "--output",
            str(out_path),
        ]
    )
    assert code == 1  # Should fail gracefully

    os.chmod(ro_dir, 0o755)  # Cleanup


def test_main_stdout_output(monkeypatch, capsys):
    """Test CLI output to stdout (no --output flag)."""
    from cli import main

    monkeypatch.setattr(
        sys.modules["decoder"], "fetch_text", lambda *a, **k: "Start <b>secret</b> end"
    )
    code = main(
        ["--source-url", "http://x", "--marker-start", "<b>", "--marker-end", "</b>"]
    )

    assert code == 0
    captured = capsys.readouterr()
    assert "secret" in captured.out


def test_extract_large_content():
    """Test extraction with very large content."""
    large_content = "x" * 10_000_000  # 10MB
    text = f"Start {{* {large_content} *}} end"
    result = extract_between(text, "{*", "*}")
    assert len(result) == 10_000_000
