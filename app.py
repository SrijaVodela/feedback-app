from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

DB_PATH = os.environ.get('FEEDBACK_DB', '/data/feedback.db')

app = Flask(__name__)
app.config['DATABASE'] = DB_PATH

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

@app.before_first_request
def initialize():
    # Ensure folder exists
    db_dir = os.path.dirname(app.config['DATABASE'])
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def feedback_form():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        # Simple validation: require name and message
        return "Name and message are required", 400

    db = get_db()
    db.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    db.commit()
    return redirect(url_for('view_feedback'))

@app.route('/feedbacks', methods=['GET'])
def view_feedback():
    db = get_db()
    rows = db.execute('SELECT id, name, email, message, created_at FROM feedback ORDER BY created_at DESC').fetchall()
    return render_template('view_feedback.html', feedbacks=rows)

if __name__ == '__main__':
    # for local dev
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_DEBUG', '0') == '1')
