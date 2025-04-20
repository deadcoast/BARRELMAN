def export_markdown(tokens, filename="barrelman_syntax.md", options=None):
    """
    Export BARRELMAN tokens to Markdown format
    
    Args:
        tokens: List of BarrelmanToken objects
        filename: Output filename
        options: Dict of optional parameters (none used for markdown currently)
    """
    if options is None:
        options = {}
        
    with open(filename, 'w') as f:
        f.write("```barrelman\n")
        for token in tokens:
            # Build line with proper indentation
            indent = "    " * token.indent_level
            parts = []
            
            if token.zone_1_declaration:
                parts.append(f"{indent}{token.zone_1_declaration}")
            
            # Add relation
            if token.zone_1_relation:
                parts.append(f"{'' if parts else indent}{token.zone_1_relation} //")
            else:
                parts.append(f"{'' if parts else indent}//")
            
            # Add modifier and trigger if present
            if token.zone_2_modifier:
                parts.append(f"% {token.zone_2_modifier}")
            
            if token.zone_3_trigger:
                parts.append(f"-> {token.zone_3_trigger}")
                
            f.write(" ".join(parts) + "\n")
        f.write("```\n")
    print(f"Markdown exported to {filename}")