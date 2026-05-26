from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password123')")
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'bob', 'bob456')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h1>Login</h1>
        <form method="GET" action="/login">
            <input name="username" placeholder="Username">
            <input name="password" placeholder="Password" type="password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/login')
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    # VULNERABLE : requête SQL non sécurisée
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"[DEBUG] Query: {query}")
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"<h1>✅ Bienvenue {user[1]} !</h1>"
    else:
        return "<h1>❌ Identifiants incorrects</h1>"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
