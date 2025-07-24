#!/usr/bin/env python3
"""Run pytest suite for ADHD Focus Hub."""

import os
import sys
import pytest

# Ensure backend package path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))


def main() -> int:
    """Execute pytest for the test suite."""
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    return pytest.main([tests_dir])


if __name__ == "__main__":
    raise SystemExit(main())
