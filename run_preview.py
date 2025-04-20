from src.preview_server import run_preview_server

# Open the test file
with open('src/github_actions/tests/testcases/good_preview.bman', 'r') as f:
    content = f.read()

# Run the preview generator
run_preview_server(content)
