#!/usr/bin/env bash
# Install gfi as a GitHub CLI extension (gh gfi).
# Usage: ./install-gh-extension.sh

set -euo pipefail

EXT_NAME="gfi"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GH_EXTENSIONS_DIR="$GH_EXTENSIONS_DIR"

if [[ -z "$GH_EXTENSIONS_DIR" ]]; then
    # Default gh extensions path
    GH_EXTENSIONS_DIR="$HOME/.config/gh/extensions"
fi

EXT_DIR="$GH_EXTENSIONS_DIR/$EXT_NAME"
BIN_DIR="$HOME/.local/bin"

echo "Installing gh-$EXT_NAME extension..."

# Create bin directory
mkdir -p "$BIN_DIR"

# Create gh-gfi wrapper script
cat > "$BIN_DIR/gh-gfi" << 'EOF'
#!/usr/bin/env bash
# gfi — GitHub CLI extension wrapper
exec python -m gfi.gh_extension "$@"
EOF
chmod +x "$BIN_DIR/gh-gfi"

# Create gh extension directory
mkdir -p "$EXT_DIR"

# Symlink or copy files
ln -sf "$SCRIPT_DIR/src" "$EXT_DIR/src" 2>/dev/null || cp -r "$SCRIPT_DIR/src" "$EXT_DIR/"

echo "Installed gh-$EXT_NAME to $EXT_DIR"
echo "Add $BIN_DIR to PATH if not already:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Run with: gh gfi"
