from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Change working directory to this script's folder so portfolio.db & index.html are found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from database import init_database, add_contact, get_visitor_count, increment_visitor_count, get_all_contacts

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize database on startup
init_database()

# ── Serve frontend ──
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# ── Admin page ──
@app.route('/admin')
def admin():
    """Admin page to view all contact messages"""
    contacts = get_all_contacts()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin - Sheeba's Portfolio Messages</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #1e1b4b;
                color: #a78bfa;
                padding: 30px;
            }
            h1 {
                text-align: center;
                color: #ec4899;
                font-size: 28px;
                margin-bottom: 10px;
            }
            .stats {
                text-align: center;
                margin-bottom: 25px;
                font-size: 16px;
                color: #c4b5fd;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background: #2d2b5a;
                border-radius: 12px;
                overflow: hidden;
            }
            th, td {
                padding: 14px 16px;
                text-align: left;
                border-bottom: 1px solid #3d3b6a;
            }
            th {
                background: #3c3799;
                color: #e9d5ff;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 1px;
            }
            tr:hover td { background: #3a3870; }
            td { color: #ddd6fe; font-size: 14px; }
            .no-msg {
                text-align: center;
                padding: 40px;
                color: #7c6fbe;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <h1>📬 Contact Messages — Sheeba A</h1>
        <div class="stats">Total Messages: {{ contacts|length }}</div>
        {% if contacts %}
        <table>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message</th>
                <th>Date</th>
            </tr>
            {% for c in contacts %}
            <tr>
                <td>{{ c.id }}</td>
                <td>{{ c.name }}</td>
                <td>{{ c.email }}</td>
                <td>{{ c.message }}</td>
                <td>{{ c.created_at }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p class="no-msg">No messages yet.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, contacts=contacts)

# ── API Routes ──
@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        name    = data.get('name', '').strip()
        email   = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({'error': 'All fields are required', 'success': False}), 400

        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address', 'success': False}), 400

        success = add_contact(name, email, message)
        if success:
            return jsonify({
                'message': 'Message sent successfully! Sheeba will get back to you soon.',
                'success': True
            }), 200
        else:
            return jsonify({'error': 'Failed to save message. Please try again.', 'success': False}), 500

    except Exception as e:
        print(f"Error in contact endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'success': False}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Return visitor statistics"""
    try:
        visitor_count = increment_visitor_count()
        return jsonify({'visitors': visitor_count, 'success': True}), 200
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

if __name__ == '__main__':
    print("\n" + "="*55)
    print("  🚀  Sheeba A — Portfolio Server Starting…")
    print("="*55)
    print("  🌐  Open:   http://localhost:5000")
    print("  📬  Admin:  http://localhost:5000/admin")
    print("  ❤️   Stop:   Press Ctrl + C")
    print("="*55 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
