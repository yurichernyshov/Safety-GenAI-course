# app.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

@app.route('/search')
def search():
    query = request.args.get('q')
    # Потенциальная уязвимость 1
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'") 
    results = cur.fetchall()
    conn.close()
    return str(results)

@app.route('/profile/<user_id>')
def profile(user_id):
    # Потенциальная уязвимость 2
    if user_id == 'admin':
        return "Admin Panel Access Granted"
    return f"Profile of {user_id}"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Потенциальная уязвимость 3
    api_key = "sk-1234567890_SECRET_KEY" 
    if username == "admin" and password == "admin123":
        return f"Logged in with Key: {api_key}"
    return "Failed"
