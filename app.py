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

# Service data
SERVICE_DATA = {
    'fms': {
        'title': 'Facility Management Services',
        'subtitle': 'Our Facility Management Services (FMS) ensure that your IT environment runs efficiently every day.',
        'icon': '🏢',
        'sections': [
            {
                'heading': 'What We Deliver',
                'items': [
                    'Onsite deployment of support engineer',
                    'User management, troubleshooting & system health checks',
                    'Network, hardware & software maintenance',
                    'Regular performance audits & preventive maintenance',
                    'Continuous monitoring for uptime and reliability'
                ]
            },
            {
                'heading': 'Benefits',
                'items': [
                    'Zero disruption and smooth daily operations',
                    'Lower IT downtime',
                    'Skilled engineers available on demand'
                ]
            }
        ]
    },
    'amc': {
        'title': 'Annual Maintenance Contract (AMC)',
        'subtitle': 'Year-Round Protection for Your IT Systems',
        'icon': '🔧',
        'sections': [
            {
                'heading': 'AMC Coverage',
                'items': [
                    'Servers, desktops, laptops & network equipment',
                    'Scheduled preventive maintenance',
                    'Priority break-fix support',
                    'Device performance tuning & updates',
                    'Fault diagnosis & quick resolution'
                ]
            },
            {
                'heading': 'Why Choose Suncom AMC',
                'items': [
                    'Predictable annual cost',
                    'Priority support response',
                    'Extended hardware lifespan'
                ]
            }
        ]
    },
    'antivirus': {
        'title': 'Antivirus Security Management',
        'subtitle': 'Centralized Endpoint Protection for Your Entire Organization',
        'icon': '🛡️',
        'sections': [
            {
                'heading': 'Our Security Management Includes',
                'items': [
                    'Centralized antivirus deployment & configuration',
                    'Real-time threat monitoring & alerts',
                    'Malware, ransomware & phishing protection',
                    'Automated updates across all devices',
                    'Compliance and reporting dashboards'
                ]
            },
            {
                'heading': 'Outcome for Your Business',
                'items': [
                    'Stronger cyber security posture',
                    'Zero manual intervention',
                    'Reduced risk of data breaches'
                ]
            }
        ]
    },
    'email': {
        'title': 'Professional Email Solutions',
        'subtitle': 'Secure & Business-Grade Communication Systems',
        'icon': '📧',
        'sections': [
            {
                'heading': 'Our Email Offerings',
                'items': [
                    'Business email setup for teams',
                    'Secure email with anti-spam & threat filtering',
                    'Microsoft 365 & cloud-based email solutions',
                    'Backup & email archiving options',
                    'Email migration from outdated servers'
                ]
            },
            {
                'heading': 'Why Businesses Choose Us',
                'items': [
                    'High uptime & reliability',
                    'Enhanced security',
                    'Professional identity for teams'
                ]
            }
        ]
    },
    'networking': {
        'title': 'Structured Networking Solutions',
        'subtitle': 'High-Performance LAN/WAN & System Integration',
        'icon': '🔌',
        'sections': [
            {
                'heading': 'Our Networking Capabilities',
                'items': [
                    'LAN/WAN design & implementation',
                    'Structured cabling for offices & data centers',
                    'Router, switch & access point setup',
                    'Network security configuration',
                    'System integration with existing infrastructure'
                ]
            },
            {
                'heading': 'What You Gain',
                'items': [
                    'Faster and stable connectivity',
                    'Centralized network control',
                    'Smooth multi-department communication'
                ]
            }
        ]
    }
}


def generate_service_page(service_key):
    """Generate HTML for a service detail page"""
    if service_key not in SERVICE_DATA:
        return None

    data = SERVICE_DATA[service_key]

    sections_html = ''
    for section in data['sections']:
        items_html = ''.join([
            f'''
            <li class="detail-item">
                <div class="detail-icon">✓</div>
                <div class="detail-text">{item}</div>
            </li>
            '''
            for item in section['items']
        ])

        sections_html += f'''
        <div class="service-section">
            <h3>{section['heading']}</h3>
            <ul class="details-list">
                {items_html}
            </ul>
        </div>
        '''

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']} - Suncom Technologies</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #FF8C42;
            --secondary: #000066;
            --dark: #1F2937;
            --light: #F9FAFB;
            --white: #FFFFFF;
            --gray: #6B7280;
            --accent: #3B82F6;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, 
                rgba(0, 0, 102, 0.3) 0%, 
                rgba(255, 140, 66, 0.3) 50%, 
                rgba(0, 0, 102, 0.3) 100%);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            min-height: 100vh;
        }}

        @keyframes gradientShift {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}

        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            z-index: 1000;
            padding: 0.8rem 0;
        }}

        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-container {{
            display: flex;
            align-items: center;
        }}

        .logo-image {{
            height: 60px;
            width: auto;
            transform: scaleX(1.6);
            transform-origin: left center;
        }}

        .back-btn {{
            background: var(--secondary);
            color: white;
            padding: 0.7rem 1.8rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }}

        .back-btn:hover {{
            background: var(--primary);
            transform: translateY(-2px);
        }}

        /* Hero Section */
        .hero {{
            margin-top: 80px;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, var(--secondary), var(--accent));
            color: white;
            text-align: center;
        }}

        .hero-icon {{
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{
                transform: translateY(0px);
            }}
            50% {{
                transform: translateY(-10px);
            }}
        }}

        .hero h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}

        .hero p {{
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
            opacity: 0.95;
        }}

        /* Content Section */
        .content-section {{
            max-width: 1000px;
            margin: 3rem auto;
            padding: 0 2rem;
        }}

        .service-section {{
            background: white;
            border-radius: 15px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-top: 3px solid var(--primary);
        }}

        .service-section h3 {{
            font-size: 1.6rem;
            color: var(--secondary);
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}

        .details-list {{
            list-style: none;
            display: grid;
            gap: 1rem;
        }}

        .detail-item {{
            display: flex;
            gap: 1rem;
            align-items: center;
            padding: 1.3rem 1.5rem;
            background: white;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }}

        .detail-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            border-left-color: var(--accent);
        }}

        .detail-icon {{
            font-size: 1rem;
            color: white;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 50%;
            font-weight: bold;
        }}

        .detail-text {{
            color: var(--dark);
            font-size: 1rem;
            line-height: 1.5;
            font-weight: 600;
        }}

        /* CTA Section */
        .cta-section {{
            background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 3rem;
        }}

        .cta-section h3 {{
            font-size: 2rem;
            color: var(--secondary);
            margin-bottom: 1rem;
            font-weight: 700;
        }}

        .cta-section p {{
            font-size: 1.1rem;
            color: var(--gray);
            margin-bottom: 2rem;
        }}

        .cta-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--primary);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
        }}

        .cta-btn:hover {{
            background: var(--secondary);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 140, 66, 0.3);
        }}

        /* Footer */
        footer {{
            background: var(--dark);
            color: white;
            text-align: center;
            padding: 2rem;
        }}

        footer p {{
            color: #9CA3AF;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero {{
                padding: 3rem 1.5rem;
            }}

            .hero h1 {{
                font-size: 2rem;
            }}

            .hero p {{
                font-size: 1rem;
            }}

            .hero-icon {{
                font-size: 3rem;
            }}

            .service-section {{
                padding: 1.5rem;
            }}

            .service-section h3 {{
                font-size: 1.3rem;
            }}

            .detail-item {{
                padding: 1rem 1.2rem;
            }}

            .detail-text {{
                font-size: 0.95rem;
            }}

            .cta-section h3 {{
                font-size: 1.6rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <div class="logo-container">
                <img src="/static/logos/suncom.jpg" alt="Suncom Technologies" class="logo-image">
            </div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-icon">{data['icon']}</div>
        <h1>{data['title']}</h1>
        <p>{data['subtitle']}</p>
    </section>

    <!-- Content Section -->
    <section class="content-section">
        {sections_html}
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <h3>Ready to Get Started?</h3>
        <p>Contact us today to learn how we can help your business</p>
        <a href="/#contact" class="cta-btn">Contact Us →</a>
    </section>

    <!-- Footer -->
    <footer>
        <p>&copy; 2025 Suncom Technologies Pvt. Ltd. All rights reserved.</p>
    </footer>
</body>
</html>
    '''


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


@app.route('/services/<service_key>')
def service_detail(service_key):
    """Serve individual service detail pages"""
    page_html = generate_service_page(service_key)

    if page_html is None:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Service Not Found</title></head>
        <body>
            <h1>Service Not Found</h1>
            <p>The requested service does not exist.</p>
            <a href="/">Return to Home</a>
        </body>
        </html>
        """, 404

    return page_html


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
        print(f"❌ Error: {str(e)}")
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
    print("\n  📄 Available pages:")
    print("     - Homepage: http://localhost:8000/")
    print("     - Services:")
    print("       • FMS: http://localhost:8000/services/fms")
    print("       • AMC: http://localhost:8000/services/amc")
    print("       • Antivirus: http://localhost:8000/services/antivirus")
    print("       • Email: http://localhost:8000/services/email")
    print("       • Networking: http://localhost:8000/services/networking")
    print("\n" + "=" * 70 + "\n")

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
            print("\n❌ Port 8000 is already in use!")
            print("   Try these solutions:")
            print("   1. Close other applications using port 8000")
            print("   2. Change port in code: app.run(port=5000)")
            print("   3. Kill the process: lsof -ti:8000 | xargs kill -9\n")
        else:
            print(f"\n❌ Error starting server: {e}\n")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!\n")