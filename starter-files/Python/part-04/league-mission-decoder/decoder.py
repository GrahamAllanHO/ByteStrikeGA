"""Decode logic for extracting text between markers from fetched URLs."""

import ipaddress
import logging
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger("league_mission_decoder")

# Approved League source hosts (exact match or subdomain). Edit as needed.
ALLOWED_HOSTS = ("league.example.com", "httpbin.org", "raw.githubusercontent.com")


class DecodeError(Exception):
    """Raised when content cannot be fetched or decoded."""


def validate_url(url):
    """Reject non-http(s) URLs and hosts resolving to private/internal addresses (SSRF guard)."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise DecodeError("Only http(s) URLs with a host are allowed")
    host = parsed.hostname.lower().rstrip(".")
    if not any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
        raise DecodeError(f"Host not in League source allowlist: {host}")
    try:
        infos = socket.getaddrinfo(parsed.hostname, parsed.port or 80)
    except socket.gaierror as exc:
        raise DecodeError(f"Cannot resolve host: {parsed.hostname}") from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise DecodeError(f"Blocked non-public address: {ip}")


def fetch_text(url, retries=3, backoff=1.0, timeout=10, opener=urllib.request.urlopen):
    """Fetch URL text, retrying with exponential backoff."""
    if opener is urllib.request.urlopen:
        validate_url(url)
    for attempt in range(1, retries + 1):
        try:
            with opener(url, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (
            urllib.error.URLError,
            TimeoutError,
            UnicodeDecodeError,
            ValueError,
        ) as exc:
            logger.warning("Fetch attempt %d/%d failed: %s", attempt, retries, exc)
            if attempt == retries:
                raise DecodeError(
                    f"Failed to fetch {url} after {retries} attempts"
                ) from exc
            time.sleep(backoff * 2 ** (attempt - 1))
    raise DecodeError("retries must be >= 1")


def extract_between(text, start, end):
    """Return all stripped text between start and end markers using regex for multiple matches."""
    if not start or not end:
        raise DecodeError("Markers must be non-empty")
    # Escape special regex characters
    import re

    escaped_start = re.escape(start)
    escaped_end = re.escape(end)
    pattern = f"{escaped_start}\\s*(.*?)\\s*{escaped_end}"
    matches = re.findall(pattern, text)
    if not matches:
        raise DecodeError(f"No content found between {start!r} and {end!r}")
    # Return all matches joined with newlines
    return "\n".join(matches)


def decode(url, start, end, retries=3):
    return extract_between(fetch_text(url, retries=retries), start, end)
