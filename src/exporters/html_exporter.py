def export_html(tokens, filename="barrelman_syntax.html", options=None):
    """
    Export BARRELMAN tokens to HTML format

    Args:
        tokens: List of BarrelmanToken objects
        filename: Output filename
        options: Dict of optional parameters
            - dark_mode: Boolean to set dark mode (default: False)
    """
    if options is None:
        options = {}

    dark_mode = options.get("dark_mode", False)

    with open(filename, "w") as f:
        _dark_mode_html(f, dark_mode, tokens)
    print(f"HTML exported to {filename}")


def _dark_mode_html(f, dark_mode, tokens):
    # Write the HTML header
    f.write("<!DOCTYPE html>\n")
    f.write("<html><head>\n")
    f.write("<meta charset='utf-8'>\n")
    f.write("<title>BARRELMAN Syntax</title>\n")
    f.write("<link rel='stylesheet' href='../static/barrelman.css'>\n")
    f.write("<style>\n")
    f.write("body { line-height: 1.2; }\n")
    f.write(".entry { margin-bottom: 0.5em; }\n")
    f.write(".modifier, .trigger { padding-left: 3em; display: block; }\n")
    f.write("</style>\n")
    f.write("</head>\n")

    # Set theme class and open body/pre tags
    theme_class = "dark" if dark_mode else "light"
    f.write(f"<body class='{theme_class}'><pre>\n")

    # Write each token as a compact entry
    for token in tokens:
        indent = "    " * token.indent_level

        # Start entry div (everything on one line)
        f.write("<div class='entry'>")

        # Write declaration and relation
        if token.zone_1_declaration:
            if token.zone_1_relation:
                f.write(
                    f"<span class='declaration'>{indent}{token.zone_1_declaration}</span> <span class='relation'>{token.zone_1_relation} //</span>"
                )
            else:
                f.write(
                    f"<span class='declaration'>{indent}{token.zone_1_declaration}</span> <span class='relation'> //</span>"
                )
        elif token.zone_1_relation:
            f.write(f"<span class='relation'>{indent}{token.zone_1_relation} //</span>")
        else:
            f.write(f"<span class='relation'>{indent} //</span>")

        # Write modifier if present (inline)
        if token.zone_2_modifier:
            f.write(f"<span class='modifier'>% {token.zone_2_modifier}</span>")

        # Write trigger if present (inline)
        if token.zone_3_trigger:
            f.write(f"<span class='trigger'>-> {token.zone_3_trigger}</span>")

        # Close entry div with a newline
        f.write("</div>\n")

    # Close tags
    f.write("</pre></body></html>")
