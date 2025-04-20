def export_dot_graph(tokens, filename="barrelman_tree.dot", options=None):
    """
    Export BARRELMAN tokens to Graphviz DOT format
    
    Args:
        tokens: List of BarrelmanToken objects
        filename: Output filename
        options: Dict of optional parameters
            - show_outcome: Boolean to include outcome info (default: True)
            - node_shape: Shape for graph nodes (default: "box")
    """
    if options is None:
        options = {}
    
    show_outcome = options.get("show_outcome", True)
    node_shape = options.get("node_shape", "box")
    
    with open(filename, 'w') as f:
        f.write(f"digraph BARRELMAN {{\n  node [shape={node_shape} style=filled fontname=Courier];\n")
        
        # Create node structure
        for i, token in enumerate(tokens):
            label = token.zone_1_relation or "UNKNOWN"
            
            if token.zone_2_modifier:
                label += f"\\n% {token.zone_2_modifier}"
            
            if token.zone_3_trigger:
                label += f"\\n-> {token.zone_3_trigger}"
            
            if show_outcome and token.zone_4_outcome:
                label += f"\\n[{token.zone_4_outcome}]"
            
            color = "lightblue" if token.is_nesting_port else "lightgrey"
            f.write(f"  node{i} [label=\"{label}\", fillcolor={color}];\n")
            
            # Create edges based on nesting level or sequential order
            if i > 0 and token.indent_level > 0:
                # Find parent node (nearest node with indent level - 1)
                parent_idx = i - 1
                while parent_idx >= 0 and tokens[parent_idx].indent_level >= token.indent_level:
                    parent_idx -= 1
                
                if parent_idx >= 0:
                    f.write(f"  node{parent_idx} -> node{i};\n")
            elif i > 0:
                f.write(f"  node{i-1} -> node{i};\n")
        
        f.write("}\n")
    print(f"DOT graph exported to {filename}")
