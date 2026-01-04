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

# Product data
PRODUCT_DATA = {
    'microsoft': {
        'title': 'Microsoft Windows OS & Office 365 Licensing',
        'subtitle': 'Authorized Microsoft Reseller Delivering Genuine Licenses for Indian Businesses',
        'icon': '💼',
        'meta_title': 'Microsoft Windows 11 Pro & Office 365 Licensing for Business | Authorized Reseller India',
        'meta_description': 'Buy genuine Microsoft Windows OS, Office 365 & Microsoft 365 licenses for your business. Certified installation, setup, migration & enterprise support from Suncom Technologies.',
        'sections': [
            {
                'heading': 'Licenses We Provide',
                'items': [
                    'Windows 11 Pro Volume Licensing',
                    'Microsoft 365 Business Standard / Premium',
                    'Office 365 Enterprise E1 / E3 / E5',
                    'Exchange Online & SharePoint Online',
                    'Teams Collaboration Licensing'
                ]
            },
            {
                'heading': 'Why Businesses Choose Suncom',
                'items': [
                    '100% Genuine Licensing',
                    'Zero Compliance Risks',
                    'Installation, Deployment & User Management',
                    'Email Migration & Security Setup',
                    'Dedicated Post-Deployment Support'
                ]
            }
        ]
    },
    'fortinet': {
        'title': 'Fortinet Next-Generation Firewall (FortiGate)',
        'subtitle': 'Advanced FortiGate NGFW with IPS, VPN, SD-WAN & Threat Protection',
        'icon': '🛡️',
        'meta_title': 'Fortinet Firewall Dealer India | FortiGate NGFW with IPS, VPN, SD-WAN',
        'meta_description': 'Buy Fortinet FortiGate next-generation firewalls with IPS, VPN, SD-WAN & threat protection. Deployment, configuration & AMC support by certified engineers.',
        'sections': [
            {
                'heading': 'Key Features',
                'items': [
                    'Intrusion Prevention System (IPS)',
                    'SSL VPN / IPsec VPN',
                    'Web & Application Filtering',
                    'SD-WAN Optimization',
                    'Real-time Threat Protection'
                ]
            },
            {
                'heading': 'Why Buy Fortinet from Suncom',
                'items': [
                    'Certified Security Engineers',
                    'HA cluster deployment capability',
                    'Real-time monitoring & support',
                    'Configuration + policy designing',
                    'Annual maintenance & SLA-based service'
                ]
            }
        ]
    },
    'logitech': {
        'title': 'Logitech Video Conferencing Solutions',
        'subtitle': 'Professional Video Conferencing for Modern Workplaces',
        'icon': '📹',
        'meta_title': 'Logitech Video Conferencing Systems India | Rally Bar, MeetUp, PTZ Cameras',
        'meta_description': 'Logitech video conferencing systems for boardrooms, huddle rooms & hybrid teams. Installation, integration & support by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Solutions We Offer',
                'items': [
                    'Logitech Rally Bar',
                    'Logitech MeetUp (Huddle Rooms)',
                    'PTZ Pro Cameras',
                    'Speakerphones & Room Audio Systems',
                    'USB Cameras for Teams/Zoom'
                ]
            },
            {
                'heading': 'Why Organizations Choose Suncom',
                'items': [
                    'Complete room design & installation',
                    'Cabling, mounting & audio clarity setup',
                    'Microsoft Teams / Zoom Rooms integration',
                    'Multi-room deployment expertise'
                ]
            }
        ]
    },
    'aruba': {
        'title': 'HPE Aruba Switches & Wireless Access Points',
        'subtitle': 'Fast, Secure & Scalable Enterprise Wi-Fi',
        'icon': '📡',
        'meta_title': 'Aruba Switch & WiFi Access Points Dealer India | Enterprise Wireless Solutions',
        'meta_description': 'High-performance Aruba switches & access points for corporate Wi-Fi networks. Installation, structured cabling & managed services by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Our Aruba Offerings',
                'items': [
                    'Aruba Instant Access Points',
                    'Aruba CX Switches',
                    'Wireless Controller Solutions',
                    'Guest Wi-Fi & Captive Portals',
                    'VLANs, Routing & NAC Integration'
                ]
            },
            {
                'heading': 'Why Suncom is the Preferred Aruba Partner',
                'items': [
                    'Predictive Wi-Fi Planning',
                    'Heatmap Design',
                    'High-density deployment (100–500 users)',
                    'On-site installation & AMC packages'
                ]
            }
        ]
    },
    'cisco': {
        'title': 'Cisco & Meraki Routers & Switches',
        'subtitle': 'Enterprise Networking Powered by Cisco & Meraki',
        'icon': '🔌',
        'meta_title': 'Cisco & Meraki Routers and Switches India | Cloud-Managed Networking',
        'meta_description': 'Buy Cisco & Meraki cloud-managed switches and routers. Enterprise networking, configuration, SD-WAN setup & remote monitoring by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Solutions We Provide',
                'items': [
                    'Layer 2 / Layer 3 Switches',
                    'Meraki Cloud Dashboard Setup',
                    'SD-WAN & Branch Networking',
                    'VLAN Segmentation & Routing',
                    'PoE Switches for IP Phones & Cameras'
                ]
            },
            {
                'heading': 'Why Suncom',
                'items': [
                    'Multi-branch Meraki deployment expertise',
                    '24x7 monitoring services',
                    'Zero-touch provisioning',
                    'Licensed configuration & support'
                ]
            }
        ]
    },
    'apc': {
        'title': 'APC Online UPS & Power Solutions',
        'subtitle': 'Uninterrupted Power for Critical IT Infrastructure',
        'icon': '⚡',
        'meta_title': 'APC Online UPS Dealer India | Server Room & Network Power Backup',
        'meta_description': 'APC Online UPS solutions for servers, data centers and network rooms. Installation, battery support and site-level power planning by Suncom Technologies.',
        'sections': [
            {
                'heading': 'UPS Categories We Offer',
                'items': [
                    '1kVA – 20kVA Online UPS',
                    'Long backup battery packs',
                    'Rack-mounted UPS',
                    'Power distribution & surge protection'
                ]
            },
            {
                'heading': 'Why Choose Suncom',
                'items': [
                    'Load calculation & UPS sizing',
                    'Structured electrical setup',
                    'On-site installation',
                    'AMC & battery replacement services'
                ]
            }
        ]
    },
    'grandstream': {
        'title': 'Grandstream IP Phones & VoIP Systems',
        'subtitle': 'Enterprise VoIP & Communication Systems',
        'icon': '📞',
        'meta_title': 'Grandstream IP Phones & VoIP Systems India | PBX & Access Points',
        'meta_description': 'Grandstream Wi-Fi access points, IP phones, PBX systems and VoIP solutions for offices & call centers. Installation & support by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Our Offerings',
                'items': [
                    'SIP IP Phones',
                    'Wi-Fi Access Points',
                    'PBX & Call Center Solutions',
                    'VoIP Gateway Configuration'
                ]
            },
            {
                'heading': 'Why Choose Suncom',
                'items': [
                    'Call flow design',
                    'IVR Setup',
                    'Integration with CRM / Teams',
                    'AMC & ongoing support'
                ]
            }
        ]
    },
    'apple': {
        'title': 'Apple MacBook Business Devices',
        'subtitle': 'Premium Business Laptops for Leadership & Creative Teams',
        'icon': '💻',
        'meta_title': 'Apple MacBook for Business | Enterprise Devices for Professionals',
        'meta_description': 'Apple MacBook devices for executives & professional teams with enterprise setup, security configuration & support by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Solutions Include',
                'items': [
                    'Device provisioning',
                    'Security & encryption setup',
                    'MDM / Apple Business Manager',
                    'Team deployment & after-sales support'
                ]
            },
            {
                'heading': 'Why Choose Suncom',
                'items': [
                    'Authorized Apple reseller',
                    'Enterprise setup & configuration',
                    'Bulk procurement support',
                    'Dedicated account management'
                ]
            }
        ]
    },
    'synology': {
        'title': 'Synology NAS & Backup Storage Solutions',
        'subtitle': 'Secure Backup & Data Storage with Synology',
        'icon': '💾',
        'meta_title': 'Synology NAS Dealer India | Backup, Storage & Private Cloud Solutions',
        'meta_description': 'Buy Synology NAS for backup, storage, virtualization and business continuity. Installation and disaster recovery setup by Suncom Technologies.',
        'sections': [
            {
                'heading': 'Use Cases',
                'items': [
                    'Centralized File Storage',
                    'Private Cloud',
                    'RAID Backup',
                    'Disaster Recovery (DR)',
                    'Virtual Machine Hosting'
                ]
            },
            {
                'heading': 'Why Suncom',
                'items': [
                    'On-site NAS installation',
                    'Backup policy setup',
                    'Secure access configuration',
                    'Multi-site replication'
                ]
            }
        ]
    },
    'cisco-refurbished': {
        'title': 'Refurbished Cisco Switches – Grade-A',
        'subtitle': 'High-Performance Refurbished Cisco Switches',
        'icon': '♻️',
        'meta_title': 'Refurbished Cisco Switches India | Grade-A Enterprise Switches with Warranty',
        'meta_description': 'Buy Grade-A refurbished Cisco switches with warranty. Cost-effective enterprise networking for budget-conscious businesses.',
        'sections': [
            {
                'heading': 'Why Buy Refurbished',
                'items': [
                    'Budget friendly',
                    'Warranty included',
                    'Fully tested hardware',
                    'VLAN & Layer 3 support'
                ]
            },
            {
                'heading': 'Quality Assurance',
                'items': [
                    'Grade-A certified equipment',
                    'Full functional testing',
                    '90-day warranty',
                    'Technical support included'
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
            f'<li class="detail-item">{item}</li>'
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
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: #FFFFFF;
        }}

        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 1rem 0;
        }}

        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-image {{
            height: 50px;
            width: auto;
            transform: scaleX(1.6);
            transform-origin: left center;
        }}

        .back-btn {{
            background: var(--secondary);
            color: white;
            padding: 0.6rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            font-size: 0.9rem;
        }}

        .back-btn:hover {{
            background: var(--primary);
            transform: translateY(-2px);
        }}

        /* Main Container */
        .main-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            min-height: 100vh;
            margin-top: 70px;
        }}

        /* Left Content Section */
        .content-side {{
            padding: 4rem 3rem 4rem 4rem;
            background: #FAFAFA;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .content-wrapper {{
            max-width: 600px;
        }}

        .page-title {{
            font-size: 3rem;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 1.5rem;
            line-height: 1.2;
            letter-spacing: -1px;
        }}

        .page-subtitle {{
            font-size: 1.1rem;
            color: #6B7280;
            margin-bottom: 3rem;
            line-height: 1.6;
        }}

        .service-section {{
            margin-bottom: 2.5rem;
        }}

        .service-section h3 {{
            font-size: 1.3rem;
            color: var(--secondary);
            margin-bottom: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85rem;
        }}

        .details-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }}

        .detail-item {{
            padding-left: 1.5rem;
            position: relative;
            font-size: 1rem;
            color: var(--dark);
            line-height: 1.6;
        }}

        .detail-item::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }}

        .cta-button {{
            display: inline-block;
            background: var(--secondary);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 2rem;
            transition: all 0.3s;
        }}

        .cta-button:hover {{
            background: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 102, 0.2);
        }}

        /* Right Visual Section */
        .visual-side {{
            background: linear-gradient(135deg, var(--secondary) 0%, #1e3a8a 100%);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .visual-side img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.3;
            position: absolute;
            top: 0;
            left: 0;
        }}

        .visual-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            padding: 3rem;
        }}

        .visual-icon {{
            font-size: 8rem;
            margin-bottom: 2rem;
            filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
        }}

        .visual-text {{
            font-size: 2.5rem;
            font-weight: 800;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            letter-spacing: -1px;
        }}

        /* Decorative Elements */
        .deco-circle {{
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 140, 66, 0.1);
        }}

        .deco-circle-1 {{
            width: 400px;
            height: 400px;
            top: -100px;
            right: -100px;
            border: 3px solid rgba(255, 140, 66, 0.3);
        }}

        .deco-circle-2 {{
            width: 200px;
            height: 200px;
            bottom: 100px;
            left: 50px;
            background: linear-gradient(135deg, rgba(255, 140, 66, 0.15), rgba(255, 165, 0, 0.15));
        }}

        .deco-dots {{
            position: absolute;
            bottom: 50px;
            right: 50px;
            display: grid;
            grid-template-columns: repeat(4, 8px);
            gap: 8px;
        }}

        .deco-dot {{
            width: 8px;
            height: 8px;
            background: rgba(255, 140, 66, 0.4);
            border-radius: 50%;
        }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .main-container {{
                grid-template-columns: 1fr;
            }}

            .visual-side {{
                min-height: 400px;
            }}

            .content-side {{
                padding: 3rem 2rem;
            }}

            .page-title {{
                font-size: 2.5rem;
            }}
        }}

        @media (max-width: 768px) {{
            .page-title {{
                font-size: 2rem;
            }}

            .visual-icon {{
                font-size: 5rem;
            }}

            .visual-text {{
                font-size: 1.8rem;
            }}

            .content-side {{
                padding: 2rem 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <img src="/static/logos/suncom.jpg" alt="Suncom Technologies" class="logo-image">
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="main-container">
        <!-- Left Content Side -->
        <div class="content-side">
            <div class="content-wrapper">
                <h1 class="page-title">{data['title']}</h1>
                <p class="page-subtitle">{data['subtitle']}</p>

                {sections_html}

                <a href="/#contact" class="cta-button">Contact Us</a>
            </div>
        </div>

        <!-- Right Visual Side -->
        <div class="visual-side">
            <img src="/static/services/{service_key}.png" alt="{data['title']}" onerror="this.style.display='none';">

            <div class="visual-content">
                <div class="visual-icon">{data['icon']}</div>
                <div class="visual-text">{data['title'].split()[0]}<br>{data['title'].split()[1] if len(data['title'].split()) > 1 else ''}</div>
            </div>

            <!-- Decorative Elements -->
            <div class="deco-circle deco-circle-1"></div>
            <div class="deco-circle deco-circle-2"></div>
            <div class="deco-dots">
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
                <div class="deco-dot"></div>
            </div>
        </div>
    </div>
</body>
</html>
    '''


def generate_product_page(product_key):
    """Generate HTML for a product detail page"""
    if product_key not in PRODUCT_DATA:
        return None

    data = PRODUCT_DATA[product_key]

    sections_html = ''
    for section in data['sections']:
        items_html = ''.join([
            f'<li class="detail-item">{item}</li>'
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
    <title>{data.get('meta_title', data['title'])} - Suncom Technologies</title>
    <meta name="description" content="{data.get('meta_description', data['subtitle'])}">
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
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: #FFFFFF;
        }}

        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 1rem 0;
        }}

        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-image {{
            height: 50px;
            width: auto;
            transform: scaleX(1.6);
            transform-origin: left center;
        }}

        .back-btn {{
            background: var(--secondary);
            color: white;
            padding: 0.6rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            font-size: 0.9rem;
        }}

        .back-btn:hover {{
            background: var(--primary);
            transform: translateY(-2px);
        }}

        /* Main Container */
        .main-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            min-height: 100vh;
            margin-top: 70px;
        }}

        /* Left Content Section */
        .content-side {{
            padding: 4rem 3rem 4rem 4rem;
            background: #FAFAFA;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .content-wrapper {{
            max-width: 600px;
        }}

        .page-title {{
            font-size: 3rem;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 1.5rem;
            line-height: 1.2;
            letter-spacing: -1px;
        }}

        .page-subtitle {{
            font-size: 1.1rem;
            color: #6B7280;
            margin-bottom: 3rem;
            line-height: 1.6;
        }}

        .service-section {{
            margin-bottom: 2.5rem;
        }}

        .service-section h3 {{
            font-size: 1.3rem;
            color: var(--secondary);
            margin-bottom: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85rem;
        }}

        .details-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }}

        .detail-item {{
            padding-left: 1.5rem;
            position: relative;
            font-size: 1rem;
            color: var(--dark);
            line-height: 1.6;
        }}

        .detail-item::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }}

        .cta-button {{
            display: inline-block;
            background: var(--secondary);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 2rem;
            transition: all 0.3s;
        }}

        .cta-button:hover {{
            background: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 102, 0.2);
        }}

        /* Right Visual Section */
        .visual-side {{
            background: linear-gradient(135deg, #FF914D 0%, #FFA500 100%);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .visual-side img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.3;
            position: absolute;
            top: 0;
            left: 0;
        }}

        .visual-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            padding: 3rem;
        }}

        .visual-icon {{
            font-size: 8rem;
            margin-bottom: 2rem;
            filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
        }}

        .visual-text {{
            font-size: 2.5rem;
            font-weight: 800;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            letter-spacing: -1px;
        }}

        /* Decorative Elements */
        .deco-circle {{
            position: absolute;
            border-radius: 50%;
        }}

        .deco-circle-1 {{
            width: 400px;
            height: 400px;
            top: -100px;
            right: -100px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.05);
        }}

        .deco-circle-2 {{
            width: 200px;
            height: 200px;
            bottom: 100px;
            left: 50px;
            background: rgba(255, 255, 255, 0.1);
        }}

        .deco-lines {{
            position: absolute;
            bottom: 80px;
            right: 80px;
            width: 150px;
            height: 150px;
        }}

        .deco-line {{
            position: absolute;
            background: rgba(255, 255, 255, 0.3);
            height: 3px;
        }}

        .deco-line:nth-child(1) {{ width: 100px; top: 0; transform: rotate(45deg); }}
        .deco-line:nth-child(2) {{ width: 80px; top: 30px; transform: rotate(-45deg); }}
        .deco-line:nth-child(3) {{ width: 60px; top: 60px; transform: rotate(45deg); }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .main-container {{
                grid-template-columns: 1fr;
            }}

            .visual-side {{
                min-height: 400px;
            }}

            .content-side {{
                padding: 3rem 2rem;
            }}

            .page-title {{
                font-size: 2.5rem;
            }}
        }}

        @media (max-width: 768px) {{
            .page-title {{
                font-size: 2rem;
            }}

            .visual-icon {{
                font-size: 5rem;
            }}

            .visual-text {{
                font-size: 1.8rem;
            }}

            .content-side {{
                padding: 2rem 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <img src="/static/logos/suncom.jpg" alt="Suncom Technologies" class="logo-image">
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="main-container">
        <!-- Left Content Side -->
        <div class="content-side">
            <div class="content-wrapper">
                <h1 class="page-title">{data['title']}</h1>
                <p class="page-subtitle">{data['subtitle']}</p>

                {sections_html}

                <a href="/#contact" class="cta-button">Get a Quote</a>
            </div>
        </div>

        <!-- Right Visual Side -->
        <div class="visual-side">
            <img src="/static/products/{product_key}.png" alt="{data['title']}" onerror="this.style.display='none';">

            <div class="visual-content">
                <div class="visual-icon">{data['icon']}</div>
                <div class="visual-text">{data['title'].split()[0]}</div>
            </div>

            <!-- Decorative Elements -->
            <div class="deco-circle deco-circle-1"></div>
            <div class="deco-circle deco-circle-2"></div>
            <div class="deco-lines">
                <div class="deco-line"></div>
                <div class="deco-line"></div>
                <div class="deco-line"></div>
            </div>
        </div>
    </div>
</body>
</html>
    '''
    """Generate HTML for a product detail page"""
    if product_key not in PRODUCT_DATA:
        return None

    data = PRODUCT_DATA[product_key]

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
    <title>{data.get('meta_title', data['title'])} - Suncom Technologies</title>
    <meta name="description" content="{data.get('meta_description', data['subtitle'])}">
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
                rgba(255, 145, 77, 0.2) 0%, 
                rgba(0, 0, 102, 0.2) 50%, 
                rgba(255, 145, 77, 0.2) 100%);
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
            background: var(--primary);
            color: white;
            padding: 0.7rem 1.8rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }}

        .back-btn:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
        }}

        /* Hero Section */
        .hero {{
            margin-top: 80px;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #FF914D, #FFA500);
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
            border-left-color: #FFA500;
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
            background: linear-gradient(135deg, #FF914D, #FFA500);
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
            background: linear-gradient(135deg, #FFF5E6 0%, #FFE8CC 100%);
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
        <p>Contact us today for a personalized quote and consultation</p>
        <a href="/#contact" class="cta-btn">Get a Quote →</a>
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


@app.route('/products/<product_key>')
def product_detail(product_key):
    """Serve individual product detail pages"""
    page_html = generate_product_page(product_key)

    if page_html is None:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Product Not Found</title></head>
        <body>
            <h1>Product Not Found</h1>
            <p>The requested product does not exist.</p>
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
    print("\n  🛠️  Services:")
    print("       • FMS: http://localhost:8000/services/fms")
    print("       • AMC: http://localhost:8000/services/amc")
    print("       • Antivirus: http://localhost:8000/services/antivirus")
    print("       • Email: http://localhost:8000/services/email")
    print("       • Networking: http://localhost:8000/services/networking")
    print("\n  📦 Products:")
    print("       • Microsoft: http://localhost:8000/products/microsoft")
    print("       • Fortinet: http://localhost:8000/products/fortinet")
    print("       • Logitech: http://localhost:8000/products/logitech")
    print("       • Aruba: http://localhost:8000/products/aruba")
    print("       • Cisco: http://localhost:8000/products/cisco")
    print("       • APC: http://localhost:8000/products/apc")
    print("       • Grandstream: http://localhost:8000/products/grandstream")
    print("       • Apple: http://localhost:8000/products/apple")
    print("       • Synology: http://localhost:8000/products/synology")
    print("       • Cisco Refurbished: http://localhost:8000/products/cisco-refurbished")
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