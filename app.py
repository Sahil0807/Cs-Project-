import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'Arnav@12',
    'database':'RegistrationSystem'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INT PRIMARY KEY,
        event_name VARCHAR(255) NOT NULL,
        event_date DATE NOT NULL,
        event_location VARCHAR(255) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT,
        participant_name VARCHAR(255) NOT NULL,
        participant_email VARCHAR(255) NOT NULL,
        participant_phone VARCHAR(50),
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM events WHERE event_date >= %s ORDER BY event_date ASC', (date.today(),))
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
    cursor.execute('''
    INSERT INTO participants 
    (event_id, participant_name, participant_email, participant_phone) 
    VALUES (%s, %s, %s, %s)
    ''', (event_id, participant_name, participant_email, participant_phone))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")

@app.route('/event/<int:event_id>')
def view_event_participants(event_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
    event = cursor.fetchone()

    cursor.execute('SELECT * FROM participants WHERE event_id = %s', (event_id,))
    participants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('event_details.html', event=event, participants=participants)


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
