from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json

class BankAPI(BaseHTTPRequestHandler):

    def add_cors_headers(self):
        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

    def do_OPTIONS(self):

        self.send_response(200)
        self.add_cors_headers()
        self.end_headers()

    def do_GET(self):

        print(f"GET Request received: {self.path}")

        if self.path == "/accounts":

            conn = sqlite3.connect("bank.db")
            cur = conn.cursor()

            cur.execute(
                "SELECT username, balance FROM accounts"
            )

            rows = cur.fetchall()

            conn.close()

            accounts = []

            for row in rows:
                accounts.append({
                    "username": row[0],
                    "balance": row[1]
                })

            self.send_response(200)
            self.add_cors_headers()
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(accounts).encode()
            )

        elif self.path.startswith("/balance/"):

            username = self.path.split("/")[-1]

            conn = sqlite3.connect("bank.db")
            cur = conn.cursor()

            cur.execute(
                "SELECT balance FROM accounts WHERE username=?",
                (username,)
            )

            result = cur.fetchone()

            conn.close()

            if result:

                response = {
                    "username": username,
                    "balance": result[0]
                }

                self.send_response(200)
                self.add_cors_headers()
                self.send_header(
                    "Content-Type",
                    "application/json"
                )
                self.end_headers()

                self.wfile.write(
                    json.dumps(response).encode()
                )

            else:

                self.send_response(404)
                self.add_cors_headers()
                self.send_header(
                    "Content-Type",
                    "application/json"
                )
                self.end_headers()

                self.wfile.write(
                    b'{"error":"user not found"}'
                )

        else:

            self.send_response(404)
            self.add_cors_headers()
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                b'{"error":"endpoint not found"}'
            )

    def do_POST(self):

        print(f"POST Request received: {self.path}")

        if self.path == "/transfer":

            content_length = int(
                self.headers['Content-Length']
            )

            body = self.rfile.read(
                content_length
            )

            data = json.loads(
                body.decode()
            )

            sender = data["from"]
            receiver = data["to"]
            amount = data["amount"]

            conn = sqlite3.connect("bank.db")
            cur = conn.cursor()

            cur.execute(
                "SELECT balance FROM accounts WHERE username=?",
                (sender,)
            )

            result = cur.fetchone()

            if not result:

                self.send_response(404)
                self.add_cors_headers()
                self.end_headers()

                self.wfile.write(
                    b'{"error":"sender not found"}'
                )

                conn.close()
                return

            sender_balance = result[0]

            cur.execute(
                "SELECT balance FROM accounts WHERE username=?",
                (receiver,)
            )

            receiver_result = cur.fetchone()

            if not receiver_result:

                self.send_response(404)
                self.add_cors_headers()
                self.end_headers()

                self.wfile.write(
                    b'{"error":"receiver not found"}'
                )

                conn.close()
                return

            if sender_balance < amount:

                self.send_response(400)
                self.add_cors_headers()
                self.end_headers()

                self.wfile.write(
                    b'{"error":"insufficient funds"}'
                )

                conn.close()
                return

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance - ?
                WHERE username = ?
                """,
                (amount, sender)
            )

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance + ?
                WHERE username = ?
                """,
                (amount, receiver)
            )

            conn.commit()
            conn.close()

            self.send_response(200)
            self.add_cors_headers()
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                b'{"status":"transfer successful"}'
            )

        else:

            self.send_response(404)
            self.add_cors_headers()
            self.end_headers()

            self.wfile.write(
                b'{"error":"endpoint not found"}'
            )

server = HTTPServer(
    ("0.0.0.0", 8080),
    BankAPI
)

print("Bank API started on port 8080")

server.serve_forever()
