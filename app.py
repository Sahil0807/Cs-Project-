from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory data store for events
events = []

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/create', methods=['POST'])
def create():
    event_name = request.form['event_name']
    event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
    event_location = request.form['event_location']
    
    # Add the new event to the in-memory data store
    events.append((len(events) + 1, event_name, event_date, event_location))
    
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    event_id = int(request.form['event_id'])
    participant_name = request.form['participant_name']
    participant_email = request.form['participant_email']
    participant_phone = request.form['participant_phone']
    
    # Here, you would typically save the registration information to a database
    print(f"New registration: Event ID={event_id}, Name={participant_name}, Email={participant_email}, Phone={participant_phone}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)