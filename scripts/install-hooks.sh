#!/usr/bin/env bash
# Installs the pre-push hook that runs the leak scan. Run once after cloning:
#   scripts/install-hooks.sh
set -e
cd "$(dirname "$0")/.."
cat > .git/hooks/pre-push <<'EOF'
#!/usr/bin/env bash
exec "$(git rev-parse --show-toplevel)/scripts/leak_scan.sh" --history
EOF
chmod +x .git/hooks/pre-push scripts/leak_scan.sh
echo "pre-push hook installed: every push runs scripts/leak_scan.sh --history first."
