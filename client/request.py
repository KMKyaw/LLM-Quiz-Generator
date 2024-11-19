import http.server
import socketserver
import requests
from urllib.parse import urlparse, parse_qs
import json

PORT = 8000  # Port for the temporary web server

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        # Forward the request to the Flask server if the path is /transcript
        if parsed_path.path == '/transcript':
            query_params = parse_qs(parsed_path.query)
            video_id = query_params.get("video_id", [None])[0]

            # Forward the request to the Flask server
            if video_id:
                response = requests.get(f'http://10.5.210.116:5000/transcript', params={"video_id": video_id})
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing video_id parameter"}')
        else:
            # Default behavior for static files
            super().do_GET()

# Start the server on port 8000
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
