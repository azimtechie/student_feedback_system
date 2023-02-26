from flask import Flask, render_template, request, redirect, url_for
import sqlite3

conn = sqlite3.connect('mydatabase.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL,
#         is_admin INTEGER DEFAULT 0
#     )
# ''')
# cursor.execute('''
#     INSERT INTO users (username, email, password, is_admin)
#     VALUES ('mosam', 'mosam@gmail.com', 'password', 1)
# ''')
# conn.commit()
# conn.close()
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/user/login', methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=? AND password=? AND is_admin=0', (email, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return redirect(url_for('user_home'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=? AND password=? AND is_admin=1', (email, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('login'))


@app.route('/user/home')
def user_home():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Get all the faculty from the database
    c.execute("SELECT * FROM faculty")
    faculty = c.fetchall()

    # Close the database connection
    conn.close()
    return render_template('user_home.html', faculty=faculty)


@app.route('/admin/home')
def admin_home():
    # TODO: add admin home page code here
    return render_template('admin_home.html')


@app.route('/add_faculty', methods=['POST'])
def add_faculty_submit():
    # Get the form data from the request object
    name = request.form['name']
    department = request.form['department']

    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Insert the new faculty into the database
    c.execute("INSERT INTO faculty (name, department) VALUES (?, ?)", (name, department))
    conn.commit()

    # Close the database connection
    conn.close()

    # Redirect back to the add faculty page
    return redirect(url_for('admin_home'))

if __name__ == '__main__':
    app.run(debug=True)
