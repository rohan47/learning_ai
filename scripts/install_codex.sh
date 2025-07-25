#!/usr/bin/env bash
# Install the Codex CLI if it isn't already available.
set -e
if command -v codex > /dev/null 2>&1; then
  echo "Codex CLI already installed." >&2
  exit 0
fi

echo "Attempting to install Codex CLI..."
# Try official repository first; fall back to open-codex if unavailable.
if ! pip install --quiet git+https://github.com/smol-ai/codex.git; then
  echo "GitHub install failed, falling back to PyPI open-codex package." >&2
  pip install --quiet open-codex
fi

echo "Codex installation attempt complete."
