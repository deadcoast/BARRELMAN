import os

from flask import Flask, render_template_string, send_from_directory

from src.exporters.html_exporter import export_html
from src.lexer import BarrelmanLexer

# Ultra compact single-line template 
TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>BARRELMAN Preview</title>
<link rel='stylesheet' href='/static/barrelman.css'>
</head>
<body class="dark"><pre>
{% for token in tokens %}{% set indent = "    " * token.indent_level %}<div class="entry">{% if token.zone_1_declaration %}<span class="declaration">{{ indent }}{{ token.zone_1_declaration }}</span> <span class="relation">{{ token.zone_1_relation }} //</span>{% else %}<span class="relation">{{ indent }}{{ token.zone_1_relation }} //</span>{% endif %}{% if token.zone_2_modifier %}<span class="modifier">% {{ token.zone_2_modifier }}</span>{% endif %}{% if token.zone_3_trigger %}<span class="trigger">-> {{ token.zone_3_trigger }}</span>{% endif %}</div>
{% endfor %}
</pre></body>
</html>"""

def run_preview_server(content):
    """Starts a local Flask server to preview Barrelman code.

    Tokenizes the provided content, exports an HTML version, and serves
    a live preview at http://localhost:5000.
    """
    # Create a new app instance for each server run
    app = Flask(__name__)
    
    lexer = BarrelmanLexer(content)
    tokens = lexer.tokenize()
    
    # Export HTML version as well
    export_html(tokens, filename="barrelman_preview.html", options={"dark_mode": True})

    # Serve static files
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), path)

    @app.route("/")
    def preview():
        return render_template_string(TEMPLATE, tokens=tokens)

    print("[BARRELMAN Preview] Running at http://localhost:5000")
    app.run(debug=False)
