import logging
import os

from flask import Flask, jsonify, render_template_string, send_from_directory

from src.exporters.html_exporter import export_html
from src.lexer import BarrelmanLexer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Improved template with debugging info
TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>BARRELMAN Preview</title>
    <link rel='stylesheet' href='/static/barrelman.css'>
    <style>
        .debug-info {
            background: rgba(100,100,100,0.2);
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body class="dark">
    <div class="debug-info">
        <h3>BARRELMAN Preview</h3>
        <p>Tokens: {{ tokens|length }} found</p>
        {% if tokens|length == 0 %}
            <p style="color: red">No tokens found! Check your BARRELMAN syntax.</p>
        {% endif %}
        <p><a href="/debug" target="_blank">View Token Debug Info</a></p>
    </div>
    <pre>{% for token in tokens %}<div class="line">
    {%- if token.zone_1_declaration is not none -%}
        {%- if token.is_nesting_port -%}
            {{ " " * token.indent_level }}<span class="port">:^: </span>
        {%- else -%}
            {{ " " * token.indent_level }}<span class="declaration">:: </span>
        {%- endif -%}
    {%- endif -%}
    
    {%- if token.zone_1_relation is not none -%}
        {%- if " // " in token.zone_1_relation -%}
            {%- set parts = token.zone_1_relation.split(" // ", 1) -%}
            <span class="keyword">{{ parts[0] }}</span><span class="relation"> // </span><span class="function">{{ parts[1] }}</span>
        {%- else -%}
            <span class="keyword">{{ token.zone_1_relation }}</span><span class="relation"> // </span>
        {%- endif -%}
    {%- endif -%}
    
    {%- if token.zone_2_modifier is not none -%}
        <span class="modifier-symbol">% </span><span class="parameter">{{ token.zone_2_modifier }}</span>
    {%- endif -%}
    
    {%- if token.zone_3_trigger is not none -%}
        <span class="trigger-symbol"> -> </span><span class="outcome">{{ token.zone_3_trigger }}</span>
    {%- endif -%}
</div>{% endfor %}</pre>

<script>
// Debug script
console.log("Token count: {{ tokens|length }}");
</script>
</body>
</html>"""


def run_preview_server(content):
    """Starts a local Flask server to preview Barrelman code.

    Tokenizes the provided content, exports an HTML version, and serves
    a live preview at http://localhost:5000.
    """
    # Create a new app instance for each server run
    app = Flask(__name__)

    # Enable logging for Flask
    app.logger.setLevel(logging.INFO)

    try:
        lexer = BarrelmanLexer(content)
        tokens = lexer.tokenize()
        logger.info(f"Tokenized {len(tokens)} tokens from content")

        # Debug token information
        for i, token in enumerate(tokens):
            logger.info(
                f"Token {i}: declaration='{token.zone_1_declaration}', relation='{token.zone_1_relation}', indent={token.indent_level}, is_port={token.is_nesting_port}")

        # Check if we actually have tokens
        if not tokens:
            logger.warning(
                "No tokens found in the content. Check BARRELMAN syntax.")

        # Export HTML version as well
        export_html(tokens, filename="barrelman_preview.html",
                    options={"dark_mode": True})
        logger.info("HTML exported to barrelman_preview.html")
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")
        tokens = []  # Empty tokens to prevent template rendering errors

    # Get the absolute path to the static directory
    static_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "static")
    logger.info(f"Static directory: {static_dir}")

    if not os.path.exists(static_dir):
        logger.error(f"Static directory does not exist: {static_dir}")
        try:
            os.makedirs(static_dir)
            logger.info(f"Created static directory: {static_dir}")
        except Exception as e:
            logger.error(f"Error creating static directory: {str(e)}")

    # Serve static files
    @app.route("/static/<path:path>")
    def send_static(path):
        logger.info(f"Request for static file: {path}")
        if os.path.exists(os.path.join(static_dir, path)):
            logger.info(f"Static file found: {path}")
        else:
            logger.error(f"Static file not found: {path}")
        return send_from_directory(static_dir, path)

    @app.route("/debug")
    def debug_tokens():
        """Return detailed token information for debugging"""
        token_info = []
        for i, token in enumerate(tokens):
            token_info.append({
                "index": i,
                "raw_line": token.line,
                "declaration": str(token.zone_1_declaration),
                "is_nesting_port": token.is_nesting_port,
                "relation": str(token.zone_1_relation),
                "indent_level": token.indent_level,
                "modifier": str(token.zone_2_modifier),
                "trigger": str(token.zone_3_trigger),
                "outcome": str(token.zone_4_outcome)
            })

        return jsonify({
            "tokens": token_info,
            "total_tokens": len(tokens)
        })

    @app.route("/")
    def preview():
        logger.info("Preview request received")
        return render_template_string(TEMPLATE, tokens=tokens)

    @app.route("/api/status")
    def status():
        return jsonify({
            "status": "ok",
            "token_count": len(tokens),
            "static_dir": static_dir,
            "static_dir_exists": os.path.exists(static_dir)
        })

    print("[BARRELMAN Preview] Running at http://localhost:5000")
    logger.info("Preview server starting")

    # Run with threaded=True to handle multiple requests and debug=False to avoid auto-reloading
    app.run(debug=False, threaded=True)
