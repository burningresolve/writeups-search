#!/usr/bin/env python3
"""search_writeups — search Pentester Land writeups by vulnerability name.

Fetches the Pentester Land writeup dataset at runtime, filters writeups
by vulnerability name, and saves matching writeup links as Markdown
task lists. The dataset is never stored locally.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

VERSION = "0.2.0"
DATA_URL = "https://pentester.land/writeups.json"

# Subtle accents approximating the macOS Dark palette.
RESET = "\033[0m"
BOLD = "\033[1m"
STYLES = {
    "info": "\033[38;5;75m",   # muted blue
    "ok": "\033[38;5;114m",    # soft green
    "warn": "\033[38;5;179m",  # muted gold
    "err": "\033[38;5;203m",   # soft red
}
MARKERS = {"info": "[*]", "ok": "[+]", "warn": "[!]", "err": "[x]"}
COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(style, text):
    return f"{STYLES[style]}{text}{RESET}" if COLOR else text


def bold(text):
    return f"{BOLD}{text}{RESET}" if COLOR else text


def say(style, text):
    print(f"{paint(style, MARKERS[style])} {text}")


def fetch_writeups():
    """Fetch and parse the remote dataset (kept in memory only)."""
    request = urllib.request.Request(
        DATA_URL, headers={"User-Agent": f"search_writeups/{VERSION}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)["data"]
    except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
        say("err", f"Failed to fetch Pentester Land data: {exc}")
        sys.exit(1)


def collect_tags(writeups):
    """Map lowercased tag to a display form, first casing seen."""
    tags = {}
    for entry in writeups:
        for name in entry.get("Bugs") or ():
            tags.setdefault(name.lower(), name)
    return tags


def find_links(writeups, target):
    """Unique (title, url) pairs for writeups tagged with target."""
    links, seen = [], set()
    for entry in writeups:
        bugs = [b.lower() for b in entry.get("Bugs") or ()]
        if target not in bugs:
            continue
        for link in entry.get("Links") or ():
            url = link.get("Link")
            if not url or url in seen:
                continue
            seen.add(url)
            links.append((link.get("Title") or url, url))
    return links


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".md"


def render_markdown(name, links):
    lines = [f"# {name}", ""]
    lines.extend(f"- [ ] [{title}]({url})" for title, url in links)
    return "\n".join(lines) + "\n"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="search_writeups",
        description="Search Pentester Land writeups by vulnerability name.",
        epilog=(
            "examples:\n"
            '  search_writeups -b "rce, SQL injection, xss"\n'),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version",
                        version=VERSION)
    search = parser.add_mutually_exclusive_group()
    search.add_argument("-t", "--tags", action="store_true",
                        help="list all available vulnerability tags")
    search.add_argument("-b", "--b", metavar="names",
                        help="vulnerability names to search, comma-separated")
    parser.add_argument("-o", "--output", metavar="file",
                        help="output filename (single vulnerability only)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.tags and not args.b:
        parser.error("specify -t/--tags or -b/--b")

    say("info", "Fetching Pentester Land writeups...")
    writeups = fetch_writeups()
    tags = collect_tags(writeups)

    if args.tags:
        for name in sorted(tags.values(), key=str.lower):
            print(name)
        return

    names = [n.strip() for n in args.b.split(",") if n.strip()]
    if not names:
        say("err", "No vulnerability name was provided.")
        sys.exit(1)
    if args.output and len(names) > 1:
        say("err", "-o/--output can only be used with a single vulnerability.")
        sys.exit(1)

    unique = {}
    for name in names:
        unique.setdefault(name.lower(), name)  # avoid overwriting files

    for name in unique.values():
        if name.lower() not in tags:
            say("warn", f"Invalid vulnerability name: {name} (skipped)")
            continue
        say("info", f"Searching: {name}")
        links = find_links(writeups, name.lower())
        if not links:
            say("warn", f"No writeups found for: {name} (file skipped)")
            continue
        path = args.output if args.output else slug(name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render_markdown(name, links))
        say("ok", f"Saved {bold(path)} ({len(links)} writeups)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(130)
    except BrokenPipeError:
        # Piping into head/less closed the pipe; exit quietly like cat(1).
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(141)
