import argparse
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
        if line.startswith("::") and "  ::" in line:
            return f"[Line {lineno}] ERROR: Extra spacing on nested '::' block."
        if ":^:" in line and not line.startswith(":^:") and not line.startswith(" :^:"):
            return f"[Line {lineno}] ERROR: ':^:' must be at the start of the line or have a single space before it."
        return None

    def get_indent_level(self, line: str) -> int:
        """Calculates the indentation level of a line.

        Determines the indentation level by comparing the length of the
        original line with the length of the line after removing leading
        spaces.
        """
        return len(line) - len(line.lstrip(" "))

    def infer_outcome(
        self, modifier: Optional[str], trigger: Optional[str]
    ) -> Optional[str]:
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
            original_line = line.rstrip("\n")
            stripped = original_line.lstrip()

            if not stripped:
                continue

            spacing_error = self.validate_spacing(original_line, lineno)
            if spacing_error:
                print(spacing_error)
                continue

            # Custom parsing logic for BARRELMAN syntax
            try:
                # Calculate the indent level based on leading spaces
                indent_level = len(original_line) - len(original_line.lstrip())

                # Check for and extract the declaration part (:: or :^:)
                # This handles both indented and non-indented declarations
                stripped_line = original_line.lstrip()
                is_nesting = False

                if stripped_line.startswith("::"):
                    declaration = "::"
                elif stripped_line.startswith(":^:"):
                    declaration = ":^:"
                    is_nesting = True
                else:
                    declaration = None

                # Remove declaration from the line
                if declaration:
                    # Extract the rest of the line without requiring a space after declaration
                    rest = stripped_line[len(declaration):].lstrip()
                else:
                    rest = stripped_line

                # Initialize token components
                relation = None
                modifier = None
                trigger = None

                # CORRECTED PARSING LOGIC FOR BARRELMAN SYNTAX

                # Step 1: Find relation marker //
                relation_idx = rest.find("//")
                if relation_idx != -1:
                    # Everything before // is the KEYWORD
                    keyword = rest[:relation_idx].strip()
                    rest_after_relation = rest[relation_idx+2:].strip()

                    # Step 2: Find modifier marker %
                    modifier_idx = rest_after_relation.find("%")
                    if modifier_idx != -1:
                        # Everything between // and % is the FUNCTION
                        function = rest_after_relation[:modifier_idx].strip()

                        # Store the KEYWORD as the relation for now
                        relation = keyword

                        # If there is FUNCTION content, add it to relation
                        if function:
                            relation = f"{keyword} // {function}"

                        # Get content after % marker - this is the PARAMETER
                        parameter_content = rest_after_relation[modifier_idx+1:].strip(
                        )

                        # Step 3: Find trigger marker ->
                        trigger_idx = parameter_content.find("->")
                        if trigger_idx != -1:
                            # Split at -> marker
                            # This is the PARAMETER
                            modifier = parameter_content[:trigger_idx].strip()
                            # This is the OUTCOME
                            trigger = parameter_content[trigger_idx+2:].strip()
                        else:
                            # No trigger, all is parameter
                            modifier = parameter_content
                    else:
                        # No % marker, check for -> marker
                        trigger_idx = rest_after_relation.find("->")
                        if trigger_idx != -1:
                            # Split at -> marker - everything before -> is FUNCTION
                            function_part = rest_after_relation[:trigger_idx].strip(
                            )
                            relation = keyword
                            if function_part:
                                # Store function as part of relation for now
                                relation = f"{keyword} // {function_part}"
                            trigger = rest_after_relation[trigger_idx+2:].strip()
                        else:
                            # No % or ->, everything after // is FUNCTION
                            relation = keyword
                            if rest_after_relation:
                                relation = f"{keyword} // {rest_after_relation}"
                else:
                    # No // marker, check for % marker
                    modifier_idx = rest.find("%")
                    if modifier_idx != -1:
                        # Split at % marker
                        relation = rest[:modifier_idx].strip()
                        modifier_content = rest[modifier_idx+1:].strip()

                        # Check for -> in modifier content
                        trigger_idx = modifier_content.find("->")
                        if trigger_idx != -1:
                            # Split at -> marker
                            modifier = modifier_content[:trigger_idx].strip()
                            trigger = modifier_content[trigger_idx+2:].strip()
                        else:
                            # No trigger, all is modifier
                            modifier = modifier_content
                    else:
                        # No // or %, check for -> marker
                        trigger_idx = rest.find("->")
                        if trigger_idx != -1:
                            # Split at -> marker
                            relation = rest[:trigger_idx].strip()
                            trigger = rest[trigger_idx+2:].strip()
                        else:
                            # No markers, everything is relation
                            relation = rest.strip()

                self.tokens.append(
                    BarrelmanToken(
                        line=original_line,
                        zone_1_declaration=declaration,
                        zone_1_relation=relation,
                        zone_2_modifier=modifier,
                        zone_3_trigger=trigger,
                        zone_4_outcome=self.infer_outcome(modifier, trigger),
                        indent_level=indent_level,
                        is_nesting_port=is_nesting,
                    )
                )
            except Exception as e:
                print(
                    f"[Line {lineno}] ERROR: Failed to parse syntax — {original_line} - {str(e)}"
                )

        return self.tokens

    def render_syntax_tree(self):
        """Renders a visual representation of the Barrelman syntax tree.

        Prints a tree-like structure to the console, showing the
        relationships between tokens based on their indentation levels
        and nesting ports.
        """

        def indent_prefix(level):
            """Generates a string prefix for indentation based on the specified level.
            Parameters:
            level (int): The indentation level, where each level adds a '│   ' prefix.

            Returns:
            str: A string representing the indentation prefix.

            Exceptions:
            None
            """
            return "│   " * level

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
            indent_spaces = " " * token.indent_level
            parts = []

            # Zone 1: Declaration
            if token.zone_1_declaration:
                if token.is_nesting_port:
                    # port color with proper spacing
                    parts.append(
                        f"{indent_spaces}\033[96m{token.zone_1_declaration}\033[0m ")
                else:
                    # declaration with proper spacing
                    parts.append(
                        f"{indent_spaces}\033[95m{token.zone_1_declaration}\033[0m ")

            # Zone 1: Keyword & Relation
            if token.zone_1_relation:
                # Check if the relation contains a function part (indicated by '//')
                if " // " in token.zone_1_relation:
                    keyword, function = token.zone_1_relation.split(" // ", 1)
                    parts.append(f"\033[94m{keyword}\033[0m")  # keyword
                    parts.append("\033[93m // \033[0m")  # relation marker
                    parts.append(f"\033[92m{function}\033[0m")  # function
                else:
                    # Just a keyword, no function
                    parts.append(
                        f"\033[94m{token.zone_1_relation}\033[0m")  # keyword
                    parts.append("\033[93m // \033[0m")  # relation marker

            # Zone 2: Modifier (Parameter)
            if token.zone_2_modifier:
                # modifier symbol with proper spacing
                parts.append("\033[92m% \033[0m")
                # parameter
                parts.append(f"\033[91m{token.zone_2_modifier}\033[0m")

            # Zone 3: Trigger (Outcome)
            if token.zone_3_trigger:
                # trigger symbol with proper spacing
                parts.append("\033[90m -> \033[0m")
                parts.append(
                    f"\033[89m{token.zone_3_trigger}\033[0m")  # outcome

            print(" ".join(parts))


# CLI tool
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BARRELMAN Lexer CLI")
    parser.add_argument("file", help="Input .bman file")
    parser.add_argument("--dot", action="store_true",
                        help="Export Graphviz .dot file")
    parser.add_argument(
        "--html", action="store_true", help="Export syntax highlighting as HTML"
    )
    parser.add_argument(
        "--markdown", action="store_true", help="Export syntax as Markdown"
    )
    parser.add_argument(
        "--highlight", action="store_true", help="Display syntax highlighted output"
    )
    parser.add_argument(
        "--dark-mode", action="store_true", help="Use dark mode for HTML export"
    )
    args = parser.parse_args()

    with open(args.file, "r") as f:
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
