#!/usr/bin/env bash
# Leak scan: fails if any term from scripts/leak_terms.txt appears anywhere in the repo.
# The term list is yours and git-ignored (it names the things you are keeping private:
# client names, email addresses, account details). One term per line, case-insensitive.
#
# Usage: scripts/leak_scan.sh            scan the working tree
#        scripts/leak_scan.sh --history  also scan every commit's diff
# Exit 0 clean, 1 on any hit. Wired to pre-push by scripts/install-hooks.sh.

set -u
cd "$(dirname "$0")/.." || exit 2
TERMS=scripts/leak_terms.txt

if [ ! -s "$TERMS" ]; then
  echo "No term list at $TERMS; nothing to scan against. Create it (one term per line) first."
  exit 2
fi

hits=0
echo "Scanning working tree against $(wc -l < "$TERMS" | tr -d ' ') terms..."
if grep -rniF -f "$TERMS" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv \
     --exclude="leak_terms.txt" . ; then
  hits=1
fi

if [ "${1:-}" = "--history" ]; then
  echo "Scanning git history..."
  if git log -p --all | grep -niF -f "$TERMS" ; then
    hits=1
  fi
fi

if [ "$hits" = 1 ]; then
  echo
  echo "LEAK SCAN FAILED: the lines above match your private term list. Fix them before pushing."
  exit 1
fi
echo "Leak scan clean."
exit 0
