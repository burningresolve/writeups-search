# writeups-search

A lightweight CLI tool for searching Pentester Land writeups by vulnerability name. `writeups-search` fetches the writeup dataset at runtime, filters it by vulnerability name, and saves matching writeups as Markdown task lists — one file per vulnerability.

## Features

- Fetch writeup data directly from Pentester Land.
- Search writeups by vulnerability name (comma-separated for multiple).
- Case-insensitive vulnerability matching.
- Report invalid names and skip them.
- List all available vulnerability tags.
- Generate a separate `.md` file per vulnerability.
- Use lowercase, hyphen-separated filenames.
- Format entries as Markdown task lists with clickable titles.
- Remove duplicate URLs within each output file.
- Preserve original titles and URLs.
- Only create output files when matching links are found.

## Requirements

- Python 3.9+ (standard library only — no dependencies)

## Installation

Make the script executable and place it on your `PATH`:

```bash
chmod +x search_writeups.py
mv search_writeups.py ~/.local/bin/search_writeups
```

## Usage

```text
usage: search_writeups [-h] [-v] [-t | -b names] [-o file]

Search Pentester Land writeups by vulnerability name.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -t, --tags            list all available vulnerability tags
  -b names, --b names   vulnerability names to search, comma-separated
  -o file, --output file
                        output filename (single vulnerability only)
```

### List all available vulnerability tags

```bash
search_writeups -t
```

### Search multiple vulnerabilities

```bash
search_writeups -b "RCE, SQL injection, XSS"
```

Each vulnerability is processed independently and produces its own output file (`rce.md`, `sql-injection.md`, `xss.md`).

## Output format

```markdown
# Race condition

- [ ] [ArtiPACKED: Hacking Giants Through a Race Condition in GitHub Actions Artifacts](https://unit42.paloaltonnetworks.com/github-repo-artifacts-leak-tokens/)
- [ ] [Race Condition About The User Version and Ignored](https://r0b0ts.medium.com/race-condition-about-the-user-version-and-ignored-c98fec642d1b)
```

Filenames are generated from the vulnerability name, lowercased and hyphen-separated: `2FA / MFA bypass` → `2fa-mfa-bypass.md`. Titles and URLs are preserved as they appear in the dataset. When no matching writeups exist, no file is created.

## Data source

`search_writeups` fetches the Pentester Land writeup dataset at runtime:

```text
https://pentester.land/writeups.json
```

The JSON is kept in memory only — it is never downloaded or stored locally.
