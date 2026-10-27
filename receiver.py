from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/webhook':
            self._send_json({"error": "Not found"}, 404)
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError):
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if not data:
            self._send_json({"error": "No data received"}, 400)
            return

        # Save test report locally
        with open('test-report.json', 'w', encoding='utf-8') as report_file:
            json.dump(data, report_file, indent=4)

        print("Test report successfully received and saved to test-report.json")
        self._send_json({"status": "success"}, 200)

    def _send_json(self, payload, status):
        response = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 5000), WebhookHandler)
    print("Webhook server listening on port 5000")
    server.serve_forever()