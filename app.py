from flask import Flask, request, render_template, redirect, url_for, flash, send_file, session
import google.generativeai as genai
import sqlite3
import json
from datetime import datetime
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages and session

# Configure Gemini API
API_KEY = "AIzaSyBCZebOrIz52leLLeUyXWpdJkDiBK9Vml0"
genai.configure(api_key=API_KEY)

# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect('submissions.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logger.debug("Database initialized.")
    except Exception as e:
        logger.error(f"DB init error: {e}")
    finally:
        conn.close()

init_db()

# HTTP server handler for contact form submissions
class ContactHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/contact':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                name = data.get('name')
                email = data.get('email')
                message = data.get('message')

                if not all([name, email, message]):
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "All fields required"}).encode('utf-8'))
                    return

                conn = sqlite3.connect('submissions.db', check_same_thread=False)
                c = conn.cursor()
                c.execute('INSERT INTO contact_submissions (name, email, message) VALUES (?, ?, ?)',
                          (name, email, message))
                conn.commit()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Form submitted successfully!"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            finally:
                conn.close()
        else:
            self.send_response(404)
            self.end_headers()

# Start HTTP server in a separate thread
def run_server():
    try:
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, ContactHandler)
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"HTTP server error: {e}")

threading.Thread(target=run_server, daemon=True).start()

# Database helper functions
def register_user(username, email, password):
    try:
        conn = sqlite3.connect('submissions.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                  (username, email, password))
        conn.commit()
        return True, "Registration successful. Please log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def login_user(username, password):
    try:
        conn = sqlite3.connect('submissions.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        return user is not None, user[1] if user else None
    except Exception as e:
        return False, None

# Routes
@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = ''
        session['logged_in'] = False
        session['generated_html'] = ''
        session['edited_html'] = ''
    try:
        conn = sqlite3.connect('submissions.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('SELECT id, name, email, message, submitted_at FROM contact_submissions')
        submissions = c.fetchall()
        conn.close()
    except Exception as e:
        flash(f"Error fetching submissions: {e}", 'error')
        submissions = []
    return render_template('index.html', 
                         logged_in=session.get('logged_in', False), 
                         username=session.get('username', ''),
                         submissions=submissions,
                         generated_html=session.get('generated_html', ''),
                         edited_html=session.get('edited_html', ''))

@app.route('/auth', methods=['POST'])
def auth():
    auth_action = request.form.get('auth_action')
    username = request.form.get('username')
    password = request.form.get('password')

    if auth_action == 'register':
        email = request.form.get('email')
        success, msg = register_user(username, email, password)
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('index'))
    
    elif auth_action == 'login':
        success, username = login_user(username, password)
        if success:
            session['logged_in'] = True
            session['username'] = username
            flash(f"Welcome {username}!", 'success')
        else:
            flash("Invalid credentials", 'error')
        return redirect(url_for('index'))
    
    elif auth_action == 'logout':
        session['logged_in'] = False
        session['username'] = ''
        session['generated_html'] = ''
        session['edited_html'] = ''
        flash("Logged out successfully", 'success')
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    initial_prompt = request.form.get('initial_prompt')
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"""
        Generate full HTML5 webpage from this prompt:
        '''{initial_prompt}'''
        Include inline CSS and JS, and return ONLY the HTML code.
        """)
        session['generated_html'] = response.text
        flash("Webpage generated successfully!", 'success')
    except Exception as e:
        flash(f"Error: {e}", 'error')
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit():
    edit_prompt = request.form.get('edit_prompt')
    if session.get('generated_html'):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            edit_response = model.generate_content(f"""
            Take this HTML:
            ```{session['generated_html']}```
            Edit it with:
            '''{edit_prompt}'''
            Return full HTML code only.
            """)
            session['edited_html'] = edit_response.text
            flash("Webpage edited successfully!", 'success')
        except Exception as e:
            flash(f"Error: {e}", 'error')
    else:
        flash("No generated webpage to edit.", 'error')
    return redirect(url_for('index'))

@app.route('/download/<file_type>')
def download(file_type):
    if file_type == 'generated' and session.get('generated_html'):
        return send_file(
            io.BytesIO(session['generated_html'].encode('utf-8')),
            as_attachment=True,
            download_name='webpage.html',
            mimetype='text/html'
        )
    elif file_type == 'edited' and session.get('edited_html'):
        return send_file(
            io.BytesIO(session['edited_html'].encode('utf-8')),
            as_attachment=True,
            download_name='edited.html',
            mimetype='text/html'
        )
    else:
        flash("No file available to download.", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    from flask_session import Session
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.run(debug=True, host='0.0.0.0', port=5000)