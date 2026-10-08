"""League mission decoder CLI.

Fetches a source URL, extracts the text between two markers, and writes it out.
Only this file is editable here, so the CLI, decode logic, and pytest tests
are kept in separate sections. Split them into cli.py, decoder.py and
test_decoder.py as needed.

README
======
Install:
    python -m pip install pytest

Usage:
    python league-mission-decoder.py --source-url https://example.com/page \
        --marker-start "BEGIN" --marker-end "END" --output result.txt

Test:
    pytest league-mission-decoder.py

Potential issues, ranked by risk (highest to lowest)
====================================================
1. Security — An untrusted source URL can access localhost or internal services
    (SSRF); the URL and destination are not restricted.
2. Security — The response is read into memory without a size limit, so a large
    response can exhaust available resources.
3. Privacy — Decoded content is printed or saved without redaction, potentially
    exposing sensitive information to terminals or persistent files.
4. Governance — There is no source allowlist or audit trail to support approved
    data-source policies and accountability.
5. Correctness — Extraction selects the first start marker and following end
    marker; repeated or ambiguous markers can yield the wrong text.
"""

import argparse
import ipaddress
import logging
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger("league_mission_decoder")
audit_logger = logging.getLogger("league_mission_decoder.audit")


def _audit_host(url):
    """Return only the hostname; never log userinfo, path, or query (may hold secrets)."""
    try:
        return urllib.parse.urlparse(url).hostname or "unknown"
    except ValueError:
        return "invalid"

# Approved League source hosts (exact match or subdomain). Edit as needed.
ALLOWED_HOSTS = ("raw.githubusercontent.com",)


# ---------------------------------------------------------------- decode logic
class DecodeError(Exception):
    """Raised when content cannot be fetched or decoded."""


def validate_url(url):
    """Reject non-http(s) URLs and hosts resolving to private/internal addresses (SSRF guard).

    Note: DNS rebinding and redirects can still bypass this check; for strong
    protection also pin the resolved IP and validate every redirect hop.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname
        port = parsed.port
    except (TypeError, ValueError) as exc:
        raise DecodeError("Invalid source URL") from exc
    if parsed.scheme not in ("http", "https") or not hostname:
        raise DecodeError("Only http(s) URLs with a host are allowed")
    if parsed.username is not None or parsed.password is not None:
        raise DecodeError("Credentials in source URLs are not allowed")
    host = hostname.lower().rstrip(".")
    if not any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
        raise DecodeError(f"Host not in League source allowlist: {host}")
    try:
        infos = socket.getaddrinfo(
            host, port or (443 if parsed.scheme == "https" else 80))
    except (OSError, ValueError) as exc:
        raise DecodeError("Cannot resolve source host") from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
            raise DecodeError(f"Blocked non-public address: {ip}")


def fetch_text(url, retries=3, backoff=1.0, timeout=10, opener=urllib.request.urlopen):
    """Fetch URL text, retrying with exponential backoff."""
    if opener is urllib.request.urlopen:
        validate_url(url)
    for attempt in range(1, retries + 1):
        try:
            with opener(url, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, OSError, TimeoutError, UnicodeDecodeError, ValueError) as exc:
            # URL-bearing exceptions may contain credentials or secret query values.
            logger.warning("Fetch attempt %d/%d failed (%s)", attempt, retries,
                           type(exc).__name__)
            if attempt == retries:
                raise DecodeError(
                    f"Failed to fetch from host {_audit_host(url)} after {retries} attempts") from exc
            time.sleep(backoff * 2 ** (attempt - 1))
    raise DecodeError("retries must be >= 1")


def extract_between(text, start, end):
    """Return the stripped text between the first start marker and the next end marker."""
    if not start or not end:
        raise DecodeError("Markers must be non-empty")
    s = text.find(start)
    if s == -1:
        raise DecodeError(f"Start marker not found: {start!r}")
    s += len(start)
    e = text.find(end, s)
    if e == -1:
        raise DecodeError(f"End marker not found: {end!r}")
    return text[s:e].strip()


def decode(url, start, end, retries=3):
    return extract_between(fetch_text(url, retries=retries), start, end)


# ------------------------------------------------------------------------- CLI
def build_parser():
    p = argparse.ArgumentParser(description="Decode a mission message from a URL.")
    p.add_argument("--source-url", required=True, help="URL to fetch")
    p.add_argument("--marker-start", required=True, help="Start marker")
    p.add_argument("--marker-end", required=True, help="End marker")
    p.add_argument("--output", help="Output file (default: stdout)")
    p.add_argument("--retries", type=int, default=3, help="Fetch retries")
    p.add_argument("--verbose", action="store_true", help="Debug logging")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )
    host = _audit_host(args.source_url)
    audit_logger.info("AUDIT decoder_run_started host=%s output=%s",
                      host, "file" if args.output else "stdout")
    try:
        result = decode(args.source_url, args.marker_start, args.marker_end, args.retries)
    except DecodeError as exc:
        audit_logger.info("AUDIT decoder_run_failed host=%s error=%s",
                          host, type(exc).__name__)
        logger.error("%s", exc)
        return 1
    audit_logger.info("AUDIT decoder_run_succeeded host=%s result_chars=%d",
                      host, len(result))
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result + "\n")
        except OSError as exc:
            logger.error("Cannot write output: %s", exc)
            return 1
        logger.info("Wrote %d characters to %s", len(result), args.output)
    else:
        print(result)
    return 0


# ----------------------------------------------------------------------- tests
def test_extract_between_ok():
    assert extract_between("xx[ hello ]yy", "[", "]") == "hello"


def test_extract_missing_start():
    import pytest
    with pytest.raises(DecodeError):
        extract_between("abc", "[", "]")


def test_extract_missing_end():
    import pytest
    with pytest.raises(DecodeError):
        extract_between("a[bc", "[", "]")


def test_fetch_retries_then_fails():
    import pytest
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
    monkeypatch.setattr(sys.modules[__name__], "fetch_text", lambda *a, **k: "A<b>secret</b>")
    out = tmp_path / "o.txt"
    code = main(["--source-url", "http://x", "--marker-start", "<b>",
                 "--marker-end", "</b>", "--output", str(out)])
    assert code == 0 and out.read_text().strip() == "secret"


if __name__ == "__main__":
    sys.exit(main())
