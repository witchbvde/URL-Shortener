from flask import Flask, render_template, request, redirect, url_for
import string
import random
import sqlite3

app = Flask(__name__)

def generate_short_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def create_database():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_id TEXT)''')
    conn.commit()
    conn.close()

def add_url_to_database(long_url, short_id):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (long_url, short_id) VALUES (?, ?)", (long_url, short_id))
    conn.commit()
    conn.close()

def get_long_url(short_id):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_id=?", (short_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_id = generate_short_id()
    add_url_to_database(long_url, short_id)
    return render_template('success.html', short_url=request.host_url + short_id)

@app.route('/<string:short_id>')
def redirect_to_long_url(short_id):
    long_url = get_long_url(short_id)
    if long_url:
        return redirect(long_url)
    return "Invalid URL"

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
