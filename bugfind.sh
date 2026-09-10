#!/usr/bin/env bash

set -o pipefail

URL="https://pentester.land/writeups.json"

usage() {
    cat << EOF
Usage:
    $0 [OPTIONS]

Description:
    Fetch Pentester Land writeups directly from the remote JSON source,
    filter writeups by vulnerability name, and save matching links
    to a local text file.

Options:
    -b, --bug <name>       Vulnerability name to search for.
    -o, --output <file>    Output file name (optional).
    -h, --help             Show this help message.

Examples:
    $0 -b "Race condition"
    $0 --bug "Race condition"

    $0 -b "RCE"
    $0 -b "SQL injection"

    $0 -b "Race condition" -o race.txt

Notes:
    - The JSON file is not downloaded or stored locally.
    - Data is fetched directly from:
      $URL
    - Search is case-insensitive.
    - By default, the output filename is generated from the bug name.

EOF
}

BUG=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--bug)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --bug requires a vulnerability name."
                echo
                usage
                exit 1
            fi

            BUG="$2"
            shift 2
            ;;

        -o|--output)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --output requires a file name."
                echo
                usage
                exit 1
            fi

            OUTPUT="$2"
            shift 2
            ;;

        -h|--help)
            usage
            exit 0
            ;;

        *)
            echo "Error: Unknown option: $1"
            echo
            usage
            exit 1
            ;;
    esac
done

if [[ -z "$BUG" ]]; then
    echo "Error: Vulnerability name is required."
    echo
    usage
    exit 1
fi

if [[ -z "$OUTPUT" ]]; then
    OUTPUT="$(
        printf '%s' "$BUG" |
        tr '[:upper:]' '[:lower:]' |
        sed 's/[^a-z0-9]/-/g; s/-\+/-/g; s/^-//; s/-$//'
    ).txt"
fi

echo "[*] Fetching writeups..."
echo "[*] Searching for: $BUG"

TEMP_FILE="$(mktemp)"

if ! curl -fsSL "$URL" | jq -r --arg bug "$BUG" '
    .data[]
    | select(
        any(
            .Bugs[]?;
            ascii_downcase | contains($bug | ascii_downcase)
        )
    )
    | .Links[]?.Link
' > "$TEMP_FILE"; then

    echo "[!] Failed to fetch or parse the JSON data."
    rm -f "$TEMP_FILE"
    exit 1
fi

mv "$TEMP_FILE" "$OUTPUT"

COUNT="$(wc -l < "$OUTPUT")"

echo
echo "[+] Vulnerability : $BUG"
echo "[+] Output        : $OUTPUT"
echo "[+] Links found   : $COUNT"
