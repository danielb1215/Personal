# Apple Wallet → finances inbox

Reads the card transactions Apple Wallet shows (Banco de Bogotá, Payoneer, Bancolombia, tap
and online) from the iPhone backup on your Mac, and writes them as a CSV into Drive
`economics/inbox`. The monthly sync on the 6th picks it up, so purchases show up in the Sheet
without waiting for card statements.

Runs only on your Mac. Nothing is uploaded except the CSV you put in Drive. The backup
password is never saved in the repo, printed or logged.

## Why it needs an encrypted backup

Wallet keeps its history in `passes23.sqlite` (`HomeDomain` → `Library/Passes/`). Finder only
includes Wallet, Health and Keychain data in a backup when "Encrypt local backup" is on.
The tool decrypts a temporary copy of that one file, reads it, and deletes the copy.

## One-time setup (~20 min)

### 1. Back up the iPhone to the Mac, encrypted, over Wi-Fi

1. Connect the iPhone with a cable, unlock it, tap **Trust**.
2. Finder → sidebar → your iPhone → **General** tab.
3. **Backups:** choose **Back up all of the data on your iPhone to this Mac**.
4. Tick **Encrypt local backup** and set a password. Save it in your password manager:
   without it the backups can't be read, by you or by this tool.
5. **Options:** tick **Show this iPhone when on Wi-Fi**. Click **Apply**.
6. Click **Back Up Now** and wait for it to finish (the first one takes a while).

After this the Mac backs up the iPhone automatically when both are on the same Wi-Fi, the
iPhone is charging and the Mac is awake (typically overnight). Check with Finder → iPhone →
"Latest backup to this Mac".

### 2. Allow access to the backup folder

macOS protects `~/Library/Application Support/MobileSync`. System Settings → Privacy & Security
→ **Full Disk Access** → add **Terminal** (for running by hand). The nightly job needs two more
entries, added in step 6.

### 3. Get the code and install the library

```bash
cd ~                                    # or wherever you keep the repo
git clone https://github.com/danielb1215/Personal.git   # skip if you already have it
cd Personal && git pull
cd tools/wallet_backup
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

(If `python3` asks to install the Command Line Tools, accept and re-run.)

### 4. Probe: check what Wallet stores (send me the output)

```bash
.venv/bin/python3 wallet_backup.py probe > ~/Desktop/wallet_probe.txt
```

It asks for the backup password (typing is hidden). The output has only the database layout,
row counts, code values, per-card counts and date ranges, and each card's issuer name and last 4
digits. No amounts, merchants, places or other values. Read it, then paste it back to Claude.
That's how we confirm that non-tap (online) purchases are there and that the codes in
`wallet_codes.json` are right.

### 5. Try an export

```bash
.venv/bin/python3 wallet_backup.py export --since 2026-09-01
```

It writes `apple_wallet_transactions.csv` into your Google Drive for desktop folder
`My Drive/economics/inbox` if that exists, or `./out/` otherwise (`--out FOLDER` to choose).
Open it and check 3–4 rows against the Wallet app (date, amount, sign, card). Purchases are
negative and refunds positive. Declined transactions are left out.

If amounts are off by a factor of 100 or 10,000, or refunds/pending look wrong, tell Claude.
The fix is a one-line change in `wallet_codes.json`.

### 6. Make it automatic (nightly)

Store the backup password in your login Keychain. This command asks for it without echoing, so
it doesn't end up in your shell history:

```bash
security add-generic-password -a "$USER" -s wallet-backup-password -T /usr/bin/security -w
```

(To change it later, add `-U`. To remove it: `security delete-generic-password -s wallet-backup-password`.)

Test the unattended path:

```bash
.venv/bin/python3 wallet_backup.py --password-from keychain export
```

Install the job, which runs daily at 06:15, or on wake if the Mac was asleep then:

```bash
chmod +x run_export.sh
sed -e "s#__TOOL_DIR__#$PWD#g" -e "s#__HOME__#$HOME#g" com.daniel.wallet-export.plist \
  > ~/Library/LaunchAgents/com.daniel.wallet-export.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.daniel.wallet-export.plist
```

Give the job Full Disk Access. System Settings → Privacy & Security → Full Disk Access → **+**,
press ⌘⇧G and add both:
- `/bin/bash`
- the real Python binary, printed by `.venv/bin/python3 -c "import os,sys; print(os.path.realpath(sys.executable))"`

Run it once now and look at the log:

```bash
launchctl kickstart gui/$(id -u)/com.daniel.wallet-export
sleep 20; tail ~/Library/Logs/wallet-export.log
```

The first time, macOS may ask whether `security` can use the Keychain item. Click **Always Allow**.

To stop it: `launchctl bootout gui/$(id -u)/com.daniel.wallet-export`.

## What the export contains

`apple_wallet_transactions.csv`, overwritten on each run. It covers the first day of last month
until today (`--since` to change), so it always overlaps the previous monthly sync, and the
sync skips rows the Sheet already has.

| column | |
|---|---|
| `wallet_txn_id` | `APW-` + hash of Wallet's own transaction id (stable when a pending purchase settles) |
| `date`, `time` | local time of the Mac |
| `card_name`, `card_last4` | issuer name on the card in Wallet; last 4 of the card number (the device number only if the card number isn't stored) |
| `merchant` | as Wallet shows it |
| `amount`, `currency` | purchase currency (for example EUR for a Banco de Bogotá purchase in Europe); purchases negative |
| `status` | `pending`, `settled`, `refund` (`unknown` if the code isn't in `wallet_codes.json`) |
| `source` | `apple_wallet` |
| `billed_amount`, `billed_currency` | only if Wallet also stores the amount in the card's currency |

## Assumptions to confirm with the probe

Apple doesn't document the Wallet database. What's known comes from forensics tools (iLEAPP
reads `payment_transaction` on iOS 13–18), and the rest is discovered from the database layout
at run time:

- **Table:** `payment_transaction`. Dates are Core Data seconds since 2001-01-01 UTC. Unix
  seconds, milliseconds and ISO text are handled too.
- **Amounts:** stored as decimal text (`"45.90"`, used as is) or as integers scaled by 10,000
  (iLEAPP's divisor, not documented by Apple; `amount_integer_scale` in `wallet_codes.json`).
  REAL values are used as is. The probe reports which storage it sees, without values.
- **Status/type codes:** `transaction_status` 0 = pending, 1 = settled, 2 = declined is a guess
  until the probe confirms it. Refunds are taken from negative amounts and from `refund_types`
  once that is known. Unrecognised codes are exported as `unknown`, never dropped.
- **Card:** found by following `<table>_pid` links from the transaction to `pass`. The name
  comes from `pass.organization_name` (or a similar column), the last 4 from
  `payment_application.fpan_suffix` (or similar). The probe prints the path it found.
- **Pending purchases:** the id stays the same when they settle, so the sync updates the
  amount in place. If the probe shows no `identifier` column, the id falls back to card + time +
  merchant + amount, and a pending purchase whose amount changes would appear twice.

## Troubleshooting

| message | fix |
|---|---|
| `macOS blocked access to the backup folder` | step 2 (Terminal) or step 6 (bash + python) Full Disk Access |
| `no iPhone backup found` | step 1, Back Up Now |
| `this backup is not encrypted` | step 1.4, then back up again |
| `wrong backup password` | the Finder backup password. For the nightly job, re-run the `security add-generic-password ... -U` command |
| `no Keychain item` | step 6 |
| `warning: the newest backup is more than 3 days old` | the iPhone hasn't backed up over Wi-Fi: leave it charging near the Mac overnight, or plug it in once |

## Tests (synthetic data only)

```bash
python3 -m unittest discover -s tests
```
