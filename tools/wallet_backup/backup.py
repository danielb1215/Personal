"""Finds the newest encrypted Finder backup and copies the Wallet database out of it.

The backup password is only ever held in memory: it is read with getpass or from the macOS
Keychain, passed to iphone_backup_decrypt, and never printed, logged or written to disk.
"""
import getpass
import glob
import os
import subprocess
import sys

BACKUP_ROOT = os.path.expanduser("~/Library/Application Support/MobileSync/Backup")
KEYCHAIN_SERVICE = "wallet-backup-password"
DOMAIN = "HomeDomain"
REL_PATH = "Library/Passes/passes23.sqlite"


class BackupError(Exception):
    pass


def newest_backup(root=BACKUP_ROOT):
    try:
        dirs = [d for d in glob.glob(os.path.join(root, "*")) if os.path.isfile(os.path.join(d, "Manifest.db"))]
    except PermissionError:
        dirs = None
    if dirs is None or (not dirs and os.path.isdir(root) and not os.access(root, os.R_OK)):
        raise BackupError("macOS blocked access to the backup folder. Give Full Disk Access to the app running "
                          "this (Terminal, or the python binary for the nightly job) - see README step 2.")
    if not dirs:
        raise BackupError(f"no iPhone backup found in {root}. Back up the iPhone in Finder first (README step 1).")
    return max(dirs, key=lambda d: os.path.getmtime(os.path.join(d, "Manifest.db")))


def password(source):
    """source: 'prompt' or 'keychain'. Never echo or log the result."""
    if source == "keychain":
        try:
            p = subprocess.run(["security", "find-generic-password", "-a", os.environ.get("USER", ""),
                                "-s", KEYCHAIN_SERVICE, "-w"], capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            raise BackupError("could not run the macOS `security` command") from None
        if p.returncode != 0:
            raise BackupError(f"no Keychain item '{KEYCHAIN_SERVICE}' for this user (README step 3)")
        return p.stdout.rstrip("\n")
    if not sys.stdin.isatty():
        raise BackupError("no terminal to ask for the backup password; use --password-from keychain")
    return getpass.getpass("iPhone backup password (not shown, not saved): ")


def extract_wallet_db(backup_dir, passphrase, out_dir):
    """Decrypts passes23.sqlite (+ its -wal/-shm journal, which holds the newest rows) into out_dir.
    Returns (db_path, [(domain, relative_path), ...] of the Wallet files seen in the manifest)."""
    try:
        from iphone_backup_decrypt import EncryptedBackup
    except ImportError:
        raise BackupError("missing library: run `pip install -r requirements.txt` in the venv (README step 4)") from None
    try:
        b = EncryptedBackup(backup_directory=backup_dir, passphrase=passphrase)
        b.test_decryption()
    except Exception as e:  # library errors never contain the passphrase; type name only to be safe
        name = type(e).__name__
        if "Passphrase" in name:
            raise BackupError("wrong backup password") from None
        if "NotEncrypted" in name:
            raise BackupError("this backup is not encrypted, so it has no Wallet data. Turn on "
                              "'Encrypt local backup' in Finder and back up again (README step 1).") from None
        raise BackupError(f"could not open the backup ({name})") from None
    with b.manifest_db_cursor() as cur:
        cur.execute("SELECT domain, relativePath FROM Files WHERE relativePath LIKE ? AND flags = 1",
                    ("%Passes/passes23.sqlite%",))
        seen = sorted(set(cur.fetchall()))
    if not seen:
        return None, []
    domain = DOMAIN if any(d == DOMAIN for d, _ in seen) else seen[0][0]
    rel = REL_PATH if (domain, REL_PATH) in seen else next(p for d, p in seen if d == domain and p.endswith(".sqlite"))
    for d, p in seen:
        if d == domain and p.startswith(rel):
            b.extract_file(relative_path=p, domain_like=d, output_filename=os.path.join(out_dir, os.path.basename(p)))
    return os.path.join(out_dir, os.path.basename(rel)), seen
