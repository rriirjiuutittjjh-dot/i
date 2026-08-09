from flask import Flask, redirect, render_template, request
import random
import sqlite3
import string

app = Flask(__name__)

# Create database if it doesn't exist
DB_NAME = 'urls.db'


def get_db_connection():
  conn = sqlite3.connect(DB_NAME, check_same_thread=False)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  conn = get_db_connection()
  conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT
        )
    ''')
  conn.commit()
  conn.close()


# Initialize the database on startup
init_db()


# Function to generate a unique short code
def generate_short_code(length=6):
  return ''.join(
      random.choices(string.ascii_letters + string.digits, k=length)
  )


# Home page to submit URL
@app.route('/', methods=['GET', 'POST'])
def home():
  short_url = None
  if request.method == 'POST':
    long_url = request.form.get('long_url', '').strip()

    if long_url:
      # Validate URL protocol
      if not (
          long_url.startswith('http://') or long_url.startswith('https://')
      ):
        long_url = 'http://' + long_url

      conn = get_db_connection()
      short_code = generate_short_code()

      # Ensure the short code is completely unique
      while (
          conn.execute(
              'SELECT id FROM urls WHERE short_code = ?', (short_code,)
          ).fetchone()
          is not None
      ):
        short_code = generate_short_code()

      # Save to DB
      conn.execute(
          'INSERT INTO urls (short_code, long_url) VALUES (?, ?)',
          (short_code, long_url),
      )
      conn.commit()
      conn.close()

      short_url = request.host_url + short_code

  return render_template('index.html', short_url=short_url)


# Redirect route
@app.route('/<short_code>')
def redirect_short_url(short_code):
  conn = get_db_connection()
  result = conn.execute(
      'SELECT long_url FROM urls WHERE short_code = ?', (short_code,)
  ).fetchone()
  conn.close()

  if result:
    return redirect(result['long_url'])
  return 'URL not found', 404


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
