from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  phone TEXT,
                  service TEXT,
                  date TEXT,
                  time TEXT,
                  UNIQUE(date, time))''')
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- BOOK ----------------
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            phone = request.form.get('phone')
            service = request.form.get('service')
            date = request.form.get('date')
            time = request.form.get('time')

            conn = sqlite3.connect('database.db')
            conn.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                         (name, phone, service, date, time))
            conn.commit()
            conn.close()

            return redirect('/success')

        except:
            return "<h3 style='color:red;'>❌ Slot already booked!</h3>"

    return render_template('book.html')

# ---------------- SUCCESS ----------------
@app.route('/success')
def success():
    return render_template('success.html')

# ---------------- ADMIN ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "1234":
            conn = sqlite3.connect('database.db')
            bookings = conn.execute("SELECT * FROM bookings").fetchall()
            conn.close()

            return render_template('dashboard.html', bookings=bookings)
        else:
            return "<h3 style='color:red;'>❌ Invalid Login</h3>"

    return render_template('admin.html')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)