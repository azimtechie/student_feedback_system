from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_bootstrap import Bootstrap


conn = sqlite3.connect('mydatabase.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         enrollment_no TEXT NOT NULL,
#         password TEXT NOT NULL,
#         is_admin INTEGER DEFAULT 0
#     )
# ''')
# cursor.execute('''
#     INSERT INTO users (username, enrollment_no, password, is_admin)
#     VALUES ('mosam', 'mosam@gmail.com', 'password', 1)
# ''')
# conn.commit()
# conn.close()
app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/user/login', methods=['POST'])
def user_login():
    enrollment_no = request.form['enrollment_no']
    password = request.form['password']
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE enrollment_no=? AND password=? AND is_admin=0', (enrollment_no, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return redirect(url_for('user_home'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/login', methods=['POST'])
def admin_login():
    print("Hello, Admin")
    enrollment_no = request.form['enrollment_no']
    password = request.form['password']
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE enrollment_no=? AND password=? AND is_admin=1', (enrollment_no, password))
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
    return render_template('adminpage.html')


@app.route('/admin/add-faculty')
def add_faculty():
    return render_template('faculty_add_form.html')


@app.route('/user/home')
def faculty_feedback():
    return render_template('user_home.html')


@app.route('/', methods=["GET", 'POST'])
def faculty_feedback_post():
    if request.method == 'POST':
        # Extract data from the form
        faculty_member = request.form['faculty_member']
        feedback_score = int(request.form['feedback_score'])

        # Insert data into the database
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute('INSERT INTO feedback (faculty_member, feedback_score) VALUES (?, ?)',
                  (faculty_member, feedback_score))
        conn.commit()
        conn.close()

        return 'Thanks for submitting your feedback!'
    # else:
    #     # Render the feedback form
    #     faculty = [('John Smith', 'Computer Science'),
    #                ('Jane Doe', 'Mathematics')]
    #     return render_template('user_home.html', faculty=faculty)


@app.route('/add_faculty', methods=['POST'])
def add_faculty_submit():
    # Get the form data from the request object
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    department = request.form['department']
    experiance = request.form['experiance']
    qualification = request.form['qualification']
    email = request.form['email']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']

    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Insert the new faculty into the database
    c.execute("INSERT INTO faculty (firstname, lastname, department, experiance, qualification, email, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (firstname, lastname, department, experiance, qualification, email, city, state, zip))
    conn.commit()

    # Close the database connection
    conn.close()

    # Redirect back to the add faculty page
    return redirect(url_for('admin_home'))


if __name__ == '__main__':
    app.run(debug=True)
