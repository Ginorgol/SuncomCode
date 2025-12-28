from flask import Flask, request, jsonify
import os
from datetime import datetime

# Create Flask app with minimal configuration
app = Flask(__name__)

# Disable any security restrictions that might cause 403
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Store contact submissions
contact_submissions = []


@app.route('/')
def index():
    """Serve the main page"""
    html_file_path = os.path.join(os.path.dirname(__file__), 'index.html')

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>File Not Found</title></head>
        <body>
            <h1>Error: index.html not found</h1>
            <p><strong>Looking for file at:</strong> {html_file_path}</p>
            <p><strong>Current directory:</strong> {os.getcwd()}</p>
            <p><strong>Script directory:</strong> {os.path.dirname(__file__)}</p>
            <p><strong>Files in current directory:</strong></p>
            <ul>
                {''.join(f'<li>{f}</li>' for f in os.listdir('.'))}
            </ul>
            <h3>Solutions:</h3>
            <ol>
                <li>Make sure index.html is in the same folder as app.py</li>
                <li>Run: <code>python app.py</code> from that folder</li>
            </ol>
        </body>
        </html>
        """, 404
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error reading file</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """, 500


@app.route('/test')
def test():
    """Simple test endpoint"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Flask Test</title></head>
    <body>
        <h1>✅ Flask is working!</h1>
        <p>If you see this, Flask is running correctly.</p>
        <p><a href="/">Go to main page</a></p>
    </body>
    </html>
    """


@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    """Handle contact form submissions"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create submission
        submission = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'message': data.get('message'),
            'timestamp': datetime.now().isoformat()
        }

        contact_submissions.append(submission)

        print(f"\n{'=' * 50}")
        print("📧 New Contact Form Submission:")
        print(f"Name: {submission['name']}")
        print(f"Email: {submission['email']}")
        print(f"Phone: {submission['phone']}")
        print(f"Message: {submission['message']}")
        print(f"{'=' * 50}\n")

        response = jsonify({
            'success': True,
            'message': 'Contact form submitted successfully'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200

    except Exception as e:
        print(f" Error: {str(e)}")
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500


@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """View all submissions"""
    return jsonify({
        'total': len(contact_submissions),
        'submissions': contact_submissions
    }), 200


@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'python_version': os.sys.version,
        'current_dir': os.getcwd(),
        'script_dir': os.path.dirname(os.path.abspath(__file__)),
        'files': os.listdir('.')
    }), 200


@app.after_request
def after_request(response):
    """Add headers to every response"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  🚀 SUNCOM TECHNOLOGIES - WEBSITE SERVER")
    print("=" * 70)

    # Try multiple configurations
    try:
        app.run(
            debug=True,
            host='0.0.0.0',  # Listen on all interfaces
            port=8000,
            use_reloader=True,
            threaded=True
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n❌ Port 5000 is already in use!")
            print("   Try these solutions:")
            print("   1. Close other applications using port 5000")
            print("   2. Change port in code: app.run(port=8000)")
            print("   3. Kill the process: lsof -ti:5000 | xargs kill -9\n")
        else:
            print(f"\n❌ Error starting server: {e}\n")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!\n")