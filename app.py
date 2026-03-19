from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  phone TEXT,
                  service TEXT,
                  date TEXT,
                  time TEXT)''')
    conn.close()

init_db()

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return "WORKING"
# -----------------------------
# BOOKING PAGE
# -----------------------------
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                     (name, phone, service, date, time))
        conn.commit()
        conn.close()

        return redirect('/success')

    return render_template('book.html')

# -----------------------------
# SUCCESS PAGE
# -----------------------------
@app.route('/success')
def success():
    return render_template('success.html')

# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('admin.html')

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    bookings = conn.execute("SELECT * FROM bookings").fetchall()
    conn.close()

    return render_template('dashboard.html', bookings=bookings)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
