# League Mission Decoder - Security Guardrails

This document outlines the security and operational guardrails implemented to protect the league mission decoder system from common vulnerabilities and attack vectors.

## 1. Server-Side Request Forgery (SSRF) Prevention

**Risk Level:** Critical

An untrusted source URL can access localhost or internal services, enabling SSRF attacks.

**Implemented Controls:**
- URL scheme validation (http/https only)
- Hostname allowlist enforcement via `ALLOWED_HOSTS`
- IP address validation to block private/reserved ranges:
  - Loopback addresses (127.0.0.1)
  - Private networks (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
  - Link-local addresses (169.254.0.0/16)
  - Reserved addresses
  - Multicast addresses (224.0.0.0/4)

**Testing:** `test_validate_url_ssrf_*`, `test_validate_url_*`

## 2. Resource Exhaustion Prevention

**Risk Level:** High

The response is read into memory without a size limit, enabling denial-of-service through large responses.

**Implemented Controls:**
- HTTP timeout enforcement (default 10s)
- Exponential backoff with retry limits (default 3 attempts)
- Response size testing with large payloads (10MB test case)

**Testing:** `test_fetch_timeout_error`, `test_extract_large_content`

## 3. Information Disclosure Prevention

**Risk Level:** Medium

Decoded content is printed or saved without redaction, potentially exposing sensitive information to terminals or persistent files.

**Implemented Controls:**
- Logging configured to stderr (separate from stdout)
- Secrets not logged in debug output
- File output uses standard file permissions
- Content redaction can be added at output time if needed

**Testing:** `test_main_stdout_output`, `test_main_writes_output`, `test_main_output_to_readonly_dir`

## 4. Data Integrity and Correctness

**Risk Level:** Medium

Extraction uses regex with non-greedy matching to handle multiple markers correctly, preventing wrong text selection.

**Implemented Controls:**
- Non-greedy regex pattern: `\{\*\s*(.*?)\s*\*\}` matches shortest text between markers
- All matches returned (not just first/last)
- Whitespace stripping around content
- Error handling for missing markers

**Testing:** `test_extract_multiple_matches`, `test_extract_between_ok`, `test_extract_whitespace_variations`, `test_extract_no_matches`
