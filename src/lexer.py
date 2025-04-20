import argparse
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BarrelmanToken:
    """Represents a token in the Barrelman language.

    A token encapsulates various components of a Barrelman statement,
    including its declaration, relation, modifier, trigger, outcome,
    indentation level, and whether it's a nesting port.
    """
    line: str
    zone_1_declaration: Optional[str]
    zone_1_relation: Optional[str]
    zone_2_modifier: Optional[str]
    zone_3_trigger: Optional[str]
    zone_4_outcome: Optional[str]
    indent_level: int = 0
    is_nesting_port: bool = False

class BarrelmanLexer:
    """Tokenizes the Barrelman source code.
    
    This method iterates through each line of the source code,
    validates spacing, extracts tokens, and appends them to the
    `tokens` list.
    """
    def __init__(self, source: str):
        """Initializes the BarrelmanLexer.

        Splits the source code into lines, initializes an empty list
        to store tokens.
        """
        self.source = source.strip().splitlines()
        self.tokens: List[BarrelmanToken] = []

    def validate_spacing(self, line: str, lineno: int) -> Optional[str]:
        """Validates spacing rules for a given line of Barrelman code.

        Checks for extra spacing on nested '::' blocks and ensures ':^:'
        is at the start of the line or has a single space before it.
        """
        if line.startswith('::') and '  ::' in line:
            return f"[Line {lineno}] ERROR: Extra spacing on nested '::' block."
        if (
            ':^:' in line
            and not line.startswith(':^:')
            and not line.startswith(' :^:')
        ):
            return f"[Line {lineno}] ERROR: ':^:' must be at the start of the line or have a single space before it."
        return None

    def get_indent_level(self, line: str) -> int:
        """Calculates the indentation level of a line.

        Determines the indentation level by comparing the length of the
        original line with the length of the line after removing leading
        spaces.
        """
        return len(line) - len(line.lstrip(' '))

    def infer_outcome(self, modifier: Optional[str], trigger: Optional[str]) -> Optional[str]:
        """Infers the outcome based on the modifier and trigger.

        Constructs an outcome string based on the presence of a modifier
        and/or a trigger.
        """
        if modifier and trigger:
            return f"Outcome inferred from % {modifier} -> {trigger}"
        elif modifier:
            return f"Modifier only outcome: {modifier}"
        elif trigger:
            return f"Trigger only outcome: {trigger}"
        return None

    def tokenize(self):
        """Tokenizes the Barrelman source code.

        This method iterates through each line of the source code,
        validates spacing, extracts tokens, and appends them to the
        `tokens` list.
        """
        for lineno, line in enumerate(self.source, start=1):
            original_line = line.rstrip('\n')
            stripped = original_line.lstrip()

            if not stripped:
                continue

            spacing_error = self.validate_spacing(original_line, lineno)
            if spacing_error:
                print(spacing_error)
                continue

            is_nesting = ':^:' in stripped

            # Custom parsing logic for BARRELMAN syntax
            try:
                # First extract the declaration part (:: or :^:)
                decl_match = re.match(r'^(::+|:^:)?', stripped)
                declaration = decl_match.group(1) if decl_match and decl_match.group(1) else None

                # Remove declaration from the line
                rest = stripped[len(declaration):].strip() if declaration else stripped

                # Split on // to separate keyword from the rest
                if '//' in rest:
                    keyword_part, rest = rest.split('//', 1)
                    keyword = keyword_part.strip()

                    # Now parse the part after //
                    # Handle special case with multiple //
                    if '//' in rest:
                        parts = rest.split('//')
                        last_part = parts[-1].strip()
                        rest = ''.join(parts[:-1]).strip()
                        if '%' in last_part or '->' in last_part:
                            rest += ' ' + last_part

                    # Extract modifier (after %) and trigger (after ->)
                    modifier = None
                    trigger = None

                    # Handle % in the remaining part
                    if '%' in rest:
                        rest_parts = rest.split('%', 1)
                        relation = rest_parts[0].strip()
                        mod_trigger = rest_parts[1].strip()

                        # Check if there's a trigger after the modifier
                        if '->' in mod_trigger:
                            mod_parts = mod_trigger.split('->', 1)
                            modifier = mod_parts[0].strip()
                            trigger = mod_parts[1].strip()
                        else:
                            modifier = mod_trigger
                    elif '->' in rest:
                        # Handle case with -> but no %
                        rest_parts = rest.split('->', 1)
                        relation = rest_parts[0].strip()
                        trigger = rest_parts[1].strip()
                    else:
                        relation = rest.strip()

                    # Combine keyword and relation if both exist
                    if relation:
                        keyword = f"{keyword} {relation}" if keyword else relation
                else:
                    # No // found, use the whole string as keyword
                    keyword = rest
                    modifier = None
                    trigger = None

                self.tokens.append(BarrelmanToken(
                    line=original_line,
                    zone_1_declaration=declaration,
                    zone_1_relation=keyword,
                    zone_2_modifier=modifier,
                    zone_3_trigger=trigger,
                    zone_4_outcome=self.infer_outcome(modifier, trigger),
                    indent_level=self.get_indent_level(original_line),
                    is_nesting_port=is_nesting
                ))
            except Exception as e:
                print(f"[Line {lineno}] ERROR: Failed to parse syntax — {original_line} - {str(e)}")

        return self.tokens

    def render_syntax_tree(self):
        """Renders a visual representation of the Barrelman syntax tree.

        Prints a tree-like structure to the console, showing the
        relationships between tokens based on their indentation levels
        and nesting ports.
        """
        def indent_prefix(level):
            """    Generates a string prefix for indentation based on the specified level.
            Parameters:
            level (int): The indentation level, where each level adds a '│   ' prefix.
            
            Returns:
            str: A string representing the indentation prefix.
            
            Exceptions: 
            None
            """
            return '│   ' * level

        print("\nBARRELMAN SYNTAX TREE:\n")
        for token in self.tokens:
            prefix = indent_prefix(token.indent_level)
            node = f"{prefix}├── {token.zone_1_relation}"
            if token.is_nesting_port:
                node += "  [PORT]"
            print(node)
            if token.zone_2_modifier:
                print(f"{prefix}│   ├── Modifier: {token.zone_2_modifier}")
            if token.zone_3_trigger:
                print(f"{prefix}│   ├── Trigger: {token.zone_3_trigger}")
            if token.zone_4_outcome:
                print(f"{prefix}│   └── Outcome: {token.zone_4_outcome}")

    def highlight(self):
        """
        Formats and prints highlighted syntax for each token in the tokens list.
    
        Parameters:
        None
        
        Returns:
        None
        
        Exceptions:
        None
        """
        print("\nBARRELMAN HIGHLIGHTED SYNTAX:\n")
        for token in self.tokens:
            parts = []
            if token.zone_1_declaration:
                parts.append(f"\033[95m{token.zone_1_declaration}\033[0m")
            parts.extend((f"\033[94m{token.zone_1_relation}\033[0m", "//"))
            if token.zone_2_modifier:
                parts.append(f"\033[92m% {token.zone_2_modifier}\033[0m")  # green
            if token.zone_3_trigger:
                parts.append(f"\033[93m-> {token.zone_3_trigger}\033[0m")  # yellow
            print(" ".join(parts))

# CLI tool
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BARRELMAN Lexer CLI")
    parser.add_argument("file", help="Input .bman file")
    parser.add_argument("--dot", action="store_true", help="Export Graphviz .dot file")
    parser.add_argument("--html", action="store_true", help="Export syntax highlighting as HTML")
    parser.add_argument("--markdown", action="store_true", help="Export syntax as Markdown")
    parser.add_argument("--highlight", action="store_true", help="Display syntax highlighted output")
    parser.add_argument("--dark-mode", action="store_true", help="Use dark mode for HTML export")
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()

    lexer = BarrelmanLexer(content)
    tokens = lexer.tokenize()

    if args.highlight:
        lexer.highlight()
    
    if args.html:
        from src.exporters.html_exporter import export_html
        export_html(tokens, options={"dark_mode": args.dark_mode})
    
    if args.markdown:
        from src.exporters.markdown_exporter import export_markdown
        export_markdown(tokens)
    
    if args.dot:
        from src.exporters.graphviz.dot_exporter import export_dot_graph
        export_dot_graph(tokens)
    
    lexer.render_syntax_tree()
