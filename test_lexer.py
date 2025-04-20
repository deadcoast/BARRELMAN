from src.lexer import BarrelmanLexer

# Sample BARRELMAN content with hierarchical structure
content = """:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
  :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
:: GENUS HOMO // 17,851 OF 302,973 % AVOID TERMINATION DURING ORGANIC CULLING PHASE
  :: GENUS HOMO // 456 OF 17,851 % TRANSCEND PLANETARY FILTER THRESHOLD
"""

# Tokenize the content
lexer = BarrelmanLexer(content)
tokens = lexer.tokenize()

# Display token information
print("TOKEN INFORMATION:")
print("-----------------")
for i, token in enumerate(tokens):
    print(f"Token {i}:")
    print(f"  Declaration: '{token.zone_1_declaration}'")
    print(f"  Relation: '{token.zone_1_relation}'")
    print(f"  Indent Level: {token.indent_level}")
    print(f"  Is Port: {token.is_nesting_port}")
    print()

# Display highlighted content
print("\nLEXER HIGHLIGHTED OUTPUT:")
print("-----------------------")
lexer.highlight()

# Manual rendering with indentation
print("\nMANUAL RENDERING WITH INDENT:")
print("---------------------------")
for token in tokens:
    indent_spaces = " " * token.indent_level
    if token.is_nesting_port:
        decl = f"{indent_spaces}\033[96m{token.zone_1_declaration}\033[0m"
    else:
        decl = f"{indent_spaces}\033[95m{token.zone_1_declaration}\033[0m"

    relation = f" \033[94m// {token.zone_1_relation}\033[0m" if token.zone_1_relation else ""
    modifier = f" \033[92m% {token.zone_2_modifier}\033[0m" if token.zone_2_modifier else ""
    trigger = f" \033[93m-> {token.zone_3_trigger}\033[0m" if token.zone_3_trigger else ""

    print(f"{decl}{relation}{modifier}{trigger}")
