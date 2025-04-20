#!/usr/bin/env python3
import argparse
import re
import sys

ZONE_REGEX = re.compile(
    r"^(\s*)(::|:\^:)?\s*(.*?)\s*//\s*(.*?)\s*(%\s+[^->\n]+)?\s*(->\s+.+)?$"
)


def parse_line(line):
    """Parses a single line of BARRELMAN syntax.

    This function takes a line of BARRELMAN syntax and parses it into its
    constituent parts, returning a dictionary containing the extracted
    information.

    Args:
        line: The line of BARRELMAN syntax to parse.

    Returns:
        A dictionary containing the parsed information, or None if the line
        does not match the expected syntax.
    """
    match = ZONE_REGEX.match(line)
    if not match:
        return None
    indent, port, decl, rel, mod, trig = match.groups()
    return {
        "indent": indent or "",
        "port": (port or "").strip(),
        "zone1": decl.strip(),
        "zone2": rel.strip(),
        "zone3": (mod or "").strip()[1:].strip() if mod else "",
        "zone4": (trig or "").strip()[2:].strip() if trig else "",
    }


def align(tokens):
    """Aligns the tokens into formatted lines.

    This function takes a list of parsed tokens and aligns them into formatted
    lines, ensuring consistent spacing and indentation.

    Args:
        tokens: A list of parsed tokens.

    Returns:
        A list of formatted lines.
    """
    col1 = max(len(t["port"] + " " + t["zone1"]) for t in tokens)
    col2 = max(len(t["zone2"]) for t in tokens)
    col3 = max(len(t["zone3"]) for t in tokens if t["zone3"])
    lines = []
    for t in tokens:
        part1 = f"{t['port']:<4} {t['zone1']}".ljust(col1 + 2)
        part2 = f"// {t['zone2']}".ljust(col2 + 4)
        part3 = f"% {t['zone3']}".ljust(col3 + 4) if t["zone3"] else ""
        part4 = f"-> {t['zone4']}" if t["zone4"] else ""
        lines.append(f"{t['indent']}{part1} {part2}{part3}{part4}".rstrip())
    return lines


def format_content(content):
    """Formats the given BARRELMAN content.

    This function takes the content of a BARRELMAN file, parses each line,
    and then aligns the parsed tokens into formatted lines.

    Args:
        content: The BARRELMAN content to format.

    Returns:
        A list of formatted lines.

    Raises:
        ValueError: If the content contains invalid BARRELMAN syntax.
    """
    lines = content.strip().splitlines()
    tokens = []
    raw_lines = []
    for line in lines:
        if not line.strip():
            raw_lines.append("")
            continue
        parsed = parse_line(line)
        if not parsed:
            raise ValueError(f"Invalid BARRELMAN syntax: {line}")
        tokens.append(parsed)
    return align(tokens)


def main():
    """Main function for the BARRELMAN formatter.

    This function parses command-line arguments, reads the input file,
    formats the content, and either checks the formatting or overwrites
    the file with the formatted content.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=".bman file to format")
    parser.add_argument(
        "--check", action="store_true", help="Check if file is properly formatted"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Auto-fix and overwrite file"
    )
    args = parser.parse_args()

    with open(args.file) as f:
        content = f.read()

    try:
        formatted = "\n".join(format_content(content)) + "\n"
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if args.check:
        if content.strip() != formatted.strip():
            print(f"[STYLE ERROR] {args.file} is not formatted.")
            sys.exit(1)
        else:
            print(f"[OK] {args.file} is properly formatted.")
    elif args.fix:
        with open(args.file, "w") as f:
            f.write(formatted)
        print(f"[FIXED] {args.file}")
    else:
        print(formatted)


if __name__ == "__main__":
    main()
