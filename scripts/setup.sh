#!/usr/bin/env bash
set -euo pipefail

# Create venv if missing
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate venv (POSIX shells)
# shellcheck source=/dev/null
source .venv/bin/activate || true

# Fallback for Git Bash on Windows
if [ ! -n "${VIRTUAL_ENV-}" ] && [ -f ".venv/Scripts/activate" ]; then
  # shellcheck disable=SC1091
  . .venv/Scripts/activate
fi

pip install -r scripts/requirements.txt

# Install pre-commit hook
HOOK_PATH=".git/hooks/pre-commit"
echo "Setting up pre-commit hook..."
cat > "$HOOK_PATH" <<'EOF'
#!/bin/bash
echo "🧹 Running pre-commit validation..."
python scripts/validate_frontmatter.py || exit 1
python scripts/build_index.py || exit 1
echo "✅ Validation passed!"
EOF
chmod +x "$HOOK_PATH"
echo "✅ Pre-commit hook installed successfully!"