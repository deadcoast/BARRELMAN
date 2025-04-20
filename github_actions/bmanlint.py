#!/usr/bin/env python3
import sys
import argparse
from bmanfmt import format_content

def lint_file(path):
    with open(path) as f:
        content = f.read()
    try:
        formatted = "\n".join(format_content(content)) + "\n"
    except ValueError as e:
        print(f"[SYNTAX ERROR] {path}: {e}")
        return 1

    if content.strip() != formatted.strip():
        print(f"[STYLE ERROR] {path} is not properly formatted.")
        return 1
    print(f"[OK] {path}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help=".bman files to check")
    args = parser.parse_args()

    errors = sum(lint_file(file) for file in args.files)
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
