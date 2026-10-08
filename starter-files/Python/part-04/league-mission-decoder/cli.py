"""CLI for league mission decoder.

Fetches a source URL, extracts the text between two markers, and writes it out.

Usage:
    python cli.py --source-url https://example.com/page \
        --marker-start "BEGIN" --marker-end "END" --output result.txt
"""

import argparse
import logging
import sys

from decoder import DecodeError, decode

# Approved League source hosts for testing
ALLOWED_HOSTS = ("league.example.com", "httpbin.org")


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
    logger = logging.getLogger("league_mission_decoder")
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )
    try:
        result = decode(
            args.source_url, args.marker_start, args.marker_end, args.retries
        )
    except DecodeError as exc:
        logger.error("%s", exc)
        return 1
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


if __name__ == "__main__":
    sys.exit(main())
