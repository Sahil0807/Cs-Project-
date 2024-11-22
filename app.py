import flask
from flask import Flask, render_template, request, redirect
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'event_registration_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Initialize database tables
def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_name VARCHAR(255) NOT NULL,
        event_date DATE NOT NULL,
        event_location VARCHAR(255) NOT NULL
    )
    ''')
    
    # Create participants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT,
        participant_name VARCHAR(255) NOT NULL,
        participant_email VARCHAR(255) NOT NULL,
        participant_phone VARCHAR(50),
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all events
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', events=events)

@app.route('/create', methods=['POST'])
def create():
    event_name = request.form['event_name']
    event_date = request.form['event_date']
    event_location = request.form['event_location']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert new event
    cursor.execute('''
    INSERT INTO events (event_name, event_date, event_location) 
    VALUES (%s, %s, %s)
    ''', (event_name, event_date, event_location))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect("/")

@app.route('/register', methods=['POST'])
def register():
    event_id = request.form['event_id']
    participant_name = request.form['participant_name']
    participant_email = request.form['participant_email']
    participant_phone = request.form['participant_phone']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert participant registration
    cursor.execute('''
    INSERT INTO participants 
    (event_id, participant_name, participant_email, participant_phone) 
    VALUES (%s, %s, %s, %s)
    ''', (event_id, participant_name, participant_email, participant_phone))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect("/")

if __name__ == '__main__':
    init_database()  # Initialize database tables
    app.run(debug=True)