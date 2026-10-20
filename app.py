import os
import time
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppass"),
    "database": os.getenv("DB_NAME", "praktikum"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_db(retries=15, delay=3):
    last_err = None
    for _ in range(retries):
        try:
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError as err:
            last_err = err
            time.sleep(delay)
    raise last_err


def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.close()


@app.route('/')
def hello():
    return "Halo dari Flask + MySQL + Docker + Jenkins!"


@app.route('/health')
def health():
    try:
        conn = get_db(retries=1, delay=0)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        conn.close()
        return jsonify(status="ok", database="connected")
    except Exception as err:
        return jsonify(status="error", database=str(err)), 500


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    conn = get_db()
    with conn.cursor() as cur:
        if request.method == 'POST':
            content = (request.get_json(silent=True) or {}).get("content", "").strip()
            if not content:
                conn.close()
                return jsonify(error="field 'content' wajib diisi"), 400
            cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
        rows = cur.fetchall()
    conn.close()
    for r in rows:
        r["created_at"] = str(r["created_at"])
    return jsonify(rows)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)