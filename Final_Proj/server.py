from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import sqlite3

conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS messages (
            sender text,
            receiver text,
            message text,
            sendTime timestamp
            )""")
conn.commit()


class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        params = parse_qs(self.path[2:])
        user = params["user"][0]
        messages_response = []
        c.execute("SELECT sender, message, sendTime FROM messages WHERE receiver=?", (user,))
        messages = c.fetchall()
        for m in messages:
            temp = {
                "sender": m[0],
                "value": m[1],
                "sendTime": m[2]
            }
            messages_response.append(temp)
        response = {
            "response": {
                "user": user,
                "messages": messages_response
            }
        }
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf_8'))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len).decode('utf-8'))
        c.execute("INSERT INTO messages VALUES (:sender, :receiver, :message, :sendTime)", post_body)
        conn.commit()
        self._set_headers()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def main():
    PORT = 80
    server_address = ('', PORT)
    server = HTTPServer(server_address, RequestHandler)
    print(f'Server running on port {PORT}')
    server.serve_forever()


if __name__ == '__main__':
    main()
