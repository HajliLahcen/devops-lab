from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import json


def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="bankdb",
        user="bankuser",
        password="bankpass"
    )


class BankAPI(BaseHTTPRequestHandler):

    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors_headers()
        self.end_headers()

    def do_GET(self):

        if self.path == "/accounts":

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT username, balance FROM accounts"
            )

            rows = cur.fetchall()

            cur.close()
            conn.close()

            accounts = []

            for row in rows:
                accounts.append({
                    "username": row[0],
                    "balance": float(row[1])
                })

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(accounts).encode()
            )

        elif self.path.startswith("/balance/"):

            username = self.path.split("/")[-1]

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
                (username,)
            )

            result = cur.fetchone()

            cur.close()
            conn.close()

            if result:

                response = {
                    "username": username,
                    "balance": float(result[0])
                }

                self.send_response(200)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps(response).encode()
                )

            else:

                self.send_response(404)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    b'{"error":"user not found"}'
                )

        else:

            self.send_response(404)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"error":"endpoint not found"}'
            )

    def do_POST(self):

        if self.path == "/transfer":

            content_length = int(
                self.headers["Content-Length"]
            )

            body = self.rfile.read(content_length)

            data = json.loads(body.decode())

            sender = data["from"]
            receiver = data["to"]
            amount = float(data["amount"])

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
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

                cur.close()
                conn.close()
                return

            sender_balance = float(result[0])

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
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

                cur.close()
                conn.close()
                return

            if sender_balance < amount:

                self.send_response(400)
                self.add_cors_headers()
                self.end_headers()

                self.wfile.write(
                    b'{"error":"insufficient funds"}'
                )

                cur.close()
                conn.close()
                return

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE username = %s
                """,
                (amount, sender)
            )

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE username = %s
                """,
                (amount, receiver)
            )

            conn.commit()

            cur.close()
            conn.close()

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
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
    ("0.0.0.0", 8000),
    BankAPI
)

print("Bank API started on port 8000")

server.serve_forever()
