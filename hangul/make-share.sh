#!/bin/sh
# Makes the shared copy (hangul/share/index.html) from hangul/index.html:
# a generic title and no preset child, so each family enters their own child's name on first open.
set -e
cd "$(dirname "$0")"
mkdir -p share
sed -e '1s|.*|<title>우리 아이 한글 놀이</title>|' \
    -e "s|^  const PRESET_CHILD = '해린';|  const PRESET_CHILD = '';|" \
    index.html > share/index.html
grep -q "const PRESET_CHILD = '';" share/index.html || { echo "PRESET_CHILD line not found" >&2; exit 1; }
