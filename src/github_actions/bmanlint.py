#!/usr/bin/env python3
import argparse
import sys

from bmanfmt import format_content


def lint_file(path):
    """Lints a single BARRELMAN file.

    This function reads the content of the file, formats it using bmanfmt,
    and checks if the original content matches the formatted content.
    If they don't match, a style error is reported.

    Args:
        path: The path to the BARRELMAN file.

    Returns:
        0 if the file is properly formatted, 1 otherwise.
    """
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
    """Main function for the BARRELMAN linter.

    This function parses command-line arguments for files to lint,
    then lints each file and exits with a non-zero status code if
    any errors are found.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help=".bman files to check")
    args = parser.parse_args()

    errors = sum(lint_file(file) for file in args.files)
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
