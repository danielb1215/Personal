#!/bin/bash
# Nightly job (started by launchd): exports Wallet transactions from the newest backup.
# Reads the backup password from the Keychain; never prints it.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') wallet export"
exec "$DIR/.venv/bin/python3" "$DIR/wallet_backup.py" --password-from keychain export "$@"
