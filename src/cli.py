import argparse

from src.exporters.graphviz.dot_exporter import export_dot_graph
from src.exporters.html_exporter import export_html
from src.exporters.markdown_exporter import export_markdown
from src.lexer import BarrelmanLexer
from src.preview_server import run_preview_server


def run_cli():
    """
    Parses command-line arguments for the BARRELMAN Lexer CLI, processes the input .bman file,
    and executes the appropriate actions based on user options (e.g., syntax highlighting,
    exporting formats, or starting a preview server).
    
    Parameters:
    None
    
    Returns:
    None
    
    Exceptions:
    Raises FileNotFoundError if the specified input file does not exist.
    """
    parser = argparse.ArgumentParser(description="BARRELMAN Lexer CLI")
    parser.add_argument("file", help="Input .bman file")
    parser.add_argument("--dot", action="store_true", help="Export Graphviz .dot file")
    parser.add_argument("--highlight", action="store_true", help="Print syntax highlighted to terminal")
    parser.add_argument("--html", action="store_true", help="Export syntax highlighting as HTML")
    parser.add_argument("--dark-mode", action="store_true", help="Enable dark mode in HTML output")
    parser.add_argument("--markdown", action="store_true", help="Export syntax highlighting as Markdown")
    parser.add_argument("--preview", action="store_true", help="Start live preview server")
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()

    lexer = BarrelmanLexer(content)
    tokens = lexer.tokenize()

    if args.highlight:
        lexer.highlight()
    if args.html:
        export_html(tokens, options={"dark_mode": args.dark_mode})
    if args.markdown:
        export_markdown(tokens)
    if args.dot:
        export_dot_graph(tokens)
    if args.preview:
        run_preview_server(content)