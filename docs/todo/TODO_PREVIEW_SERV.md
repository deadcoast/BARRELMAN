# TODO LIST FOR preview_server.py

1. [ ] Implement error handling to manage exceptions during rendering.
2. [ ] Validate and sanitize `tokens` to prevent injection attacks.
3. [ ] Use caching for the rendered template to improve performance.
4. [ ] Add error handling to return a 404 response if the file is not found.
5. [ ] Implement caching headers to improve performance for static file delivery.
6. [ ] Validate the `path` input to prevent directory traversal attacks.
7. [ ] Add error handling to manage cases where `token` attributes may be `None` or invalid.
8. [ ] Implement a logging mechanism to track the output for debugging purposes.
9. [ ] Allow customization of color codes through parameters for better user experience.
10. [ ] Add an optional parameter to customize the character used for indentation.
11. [ ] Implement error handling for negative levels to prevent unexpected behavior.
12. [ ] Include a parameter to specify the number of repetitions for the indentation.
13. [ ] Implement error handling for file operations and tokenization to ensure robustness and provide user feedback on failures.
14. [ ] Add a mechanism to allow dynamic content updates without restarting the server, such as using WebSocket or AJAX for real-time previews.
15. [ ] Include a configuration option for the server port and debug mode to enhance flexibility and usability for different environments.
