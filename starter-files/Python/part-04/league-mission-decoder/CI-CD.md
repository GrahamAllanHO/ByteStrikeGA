# League Mission Decoder - CI/CD Documentation

## Overview

The League Mission Decoder includes a comprehensive GitHub Actions CI/CD pipeline that ensures code quality, security, and containerization for production deployment.

## Pipeline Stages

### 1. **Lint** (Runs First)
- **Tool**: flake8, black
- **Purpose**: Enforces code style and catches syntax errors
- **Fails on**: Syntax errors, undefined names, formatting issues
- **Artifacts**: None

### 2. **Test & Coverage** (Depends on Lint)
- **Tool**: pytest, pytest-cov
- **Test Cases**: 34 tests (25 unit + 9 integration)
- **Coverage Target**: 80% minimum
- **Generates**:
  - Terminal report with missing lines
  - HTML coverage report
  - XML for Codecov
- **Artifacts**: `coverage-report/` HTML directory
- **Codecov Integration**: Uploads coverage for tracking

### 3. **Build Docker Image** (Depends on Test, Main Branch Only)
- **When**: Automatically on push to `main` branch
- **Base Image**: `python:3.12-slim`
- **Strategy**: Multi-stage build for minimal size
- **Features**:
  - Non-root user (uid 1000)
  - Health checks enabled
  - Metadata labels included
  - Cache optimization with GitHub Actions Cache
- **Registry**: GitHub Container Registry (ghcr.io)
- **Tags**:
  - `latest` (main branch)
  - `branch-<name>`
  - `sha-<commit-hash>`
  - Semantic versioning (v1.0.0)

### 4. **Security Scan** (Depends on Test)
- **Tools**:
  - `bandit`: Python-specific security issues
  - `safety`: Vulnerable dependencies
- **Purpose**: Identifies security vulnerabilities in code and dependencies
- **Artifacts**: `security-reports/bandit-report.json`
- **Non-blocking**: Reports issues but allows workflow to pass

### 5. **Notify** (Final, Runs Always)
- **Purpose**: Summarizes results and fails workflow if lint or tests failed
- **Status Output**:
  ```
  ✅ Lint: <passed|failed>
  ✅ Tests: <passed|failed>
  ✅ Security: <passed|failed>
  ```

## Workflow Triggers

- **Push**: On branches `main`, `develop` when files in `starter-files/Python/part-04/league-mission-decoder/` change
- **Pull Requests**: On branches targeting `main`

## Environment Variables

```yaml
REGISTRY: ghcr.io
IMAGE_NAME: ${{ github.repository }}/league-mission-decoder
```

## Test Coverage

### Current Coverage
- **decoder.py**: URL validation, fetch logic, extraction
- **cli.py**: Argument parsing, main flow, file I/O
- **test_decoder.py**: 25 unit tests for edge cases
- **test_integration.py**: 9 integration tests with mock server

### Coverage Thresholds
- **Minimum**: 80%
- **Recommendation**: Maintain above 85%

## Docker Build & Run

### Build Locally
```bash
docker build -t league-mission-decoder:latest \
  -f starter-files/Python/part-04/league-mission-decoder/Dockerfile .
```

### Run Container
```bash
# Show help
docker run --rm league-mission-decoder:latest

# Decode from URL
docker run --rm league-mission-decoder:latest \
  --source-url https://httpbin.org/html \
  --marker-start "<h1>" \
  --marker-end "</h1>"

# Save output
docker run --rm -v /tmp:/tmp league-mission-decoder:latest \
  --source-url https://httpbin.org/html \
  --marker-start "<h1>" \
  --marker-end "</h1>" \
  --output /tmp/decoded.txt
```

### Image Size
- Builder stage: ~200MB (includes test tools)
- Runtime stage: ~150MB (minimal Python runtime)

## Security Considerations

### SSRF Protection
- URL scheme validation (http/https only)
- Hostname allowlist enforcement
- Private IP blocking (loopback, RFC1918, reserved, multicast)

### Process Security
- Non-root user (decoder:1000)
- Read-only filesystem support (ready)
- Health checks configured

### Image Scanning
- Bandit for Python security issues
- Safety for dependency vulnerabilities
- SBOM labels for tracking

## Artifacts

### Coverage Report
- Location: `htmlcov/`
- Browse: Open `index.html` in browser
- Format: Line-by-line coverage with coloring

### Security Report
- Format: JSON (Bandit output)
- Tools: Bandit + Safety checks

### Docker Image
- Registry: `ghcr.io/<owner>/league-mission-decoder`
- Tags: Multiple (branch, sha, semver, latest)

## Troubleshooting

### Tests Failing
1. Run locally: `pytest -v`
2. Check coverage: `pytest --cov=decoder --cov=cli --cov-report=term-missing`
3. Review mock server: `python -m pytest test_integration.py -v -s`

### Docker Build Failing
1. Check syntax: `docker build --dry-run ...`
2. Verify requirements.txt exists
3. Test stage locally: `pip install -r requirements.txt`

### Coverage Below 80%
1. Generate HTML report: `pytest --cov --cov-report=html`
2. Open `htmlcov/index.html`
3. Identify untested paths
4. Add tests to `test_decoder.py` or `test_integration.py`

## Future Enhancements

- [ ] Add performance benchmarks
- [ ] Add integration tests against real endpoints
- [ ] Add database connectivity tests (if needed)
- [ ] Add SBOM generation (syft)
- [ ] Add image vulnerability scanning (Trivy)
- [ ] Add release automation (GitHub Releases)
- [ ] Add deployment stage (to staging/prod)

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Bandit Security Documentation](https://bandit.readthedocs.io/)
- [Pytest Coverage Documentation](https://pytest-cov.readthedocs.io/)
