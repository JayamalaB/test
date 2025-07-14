# app.py
from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session and flash messages

# MySQL Config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flask_forms',
    'port':'3307'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()
    gender_options = ['Male', 'Female', 'Other']

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        city = request.form['city']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password,gender,city) VALUES (%s, %s, %s,%s,%s)", (name, email, password,gender,city))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template('register.html',
                           id="name", name="name", label="Full Name",
                           email_id="email", email_name="email", email_label="Email Address",
                           password_id="password", password_name="password", password_label="Password",
                           select_id="gender", select_name="gender", select_label="Gender",
                           select_options=gender_options, gender_selected="",
                           radio_label="Select City", radio_name="city",
                           radio_options=cities, city_selected="")


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html',
                           email_id="email", email_name="email", email_label="Enter Email",
                           password_id="password", password_name="password", password_label="Enter Password")

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return f"<h3>Welcome, {session['user_name']}! <a href='/logout'>Logout</a></h3>"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    gender_options = ['Satisfied', 'Not satisfied']
    rating_options = [
        {'id': 1, 'name': 'Poor'},
        {'id': 2, 'name': 'Average'},
        {'id': 3, 'name': 'Good'},
        {'id': 4, 'name': 'Very Good'},
        {'id': 5, 'name': 'Excellent'}
    ]
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        feedback=request.form['feedback']
        rating = request.form['rating']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message,feedback,rating) VALUES (%s, %s, %s,%s,%s)", (name, email, message,feedback,rating))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html',
                           id="name", name="name", label="Your Name",
                           email_id="email", email_name="email", email_label="Email",
                           message_id="message", message_name="message", message_label="Message",
                           select_id="feedback", select_name="feedback", select_label="Feedback",
                           select_options=gender_options, gender_selected="",  
                           radio_label="Select Rating", radio_name="rating",
                           radio_options=rating_options, city_selected="")

if __name__ == '__main__':
    app.run(debug=True)
