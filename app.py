from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

THREAT_STATS = {
    "breaches_prevented": 14872,
    "tunnels_secured": 3241,
    "mfa_authentications": 98431,
    "uptime_percent": 99.98
}

TEAM_MEMBERS = [
    {
        "name": "Dr. Elena Vasquez",
        "role": "Chief Security Architect",
        "expertise": "Zero Trust & Identity Management",
        "icon": "shield-halved"
    },
    {
        "name": "Marcus Chen",
        "role": "Cloudflare Tunnel Engineer",
        "expertise": "Network Tunneling & Edge Security",
        "icon": "network-wired"
    },
    {
        "name": "Priya Nair",
        "role": "MFA Systems Lead",
        "expertise": "Multi-Factor Authentication & IAM",
        "icon": "key"
    },
    {
        "name": "James Okafor",
        "role": "Threat Intelligence Analyst",
        "expertise": "Penetration Testing & Red Team",
        "icon": "bug"
    }
]

ZT_PRINCIPLES = [
    {
        "title": "Verify Explicitly",
        "description": "Always authenticate and authorize based on all available data points including identity, location, device, service, and data classification.",
        "icon": "id-badge"
    },
    {
        "title": "Least Privilege Access",
        "description": "Limit user access with just-in-time and just-enough-access, risk-based adaptive policies, and data protection.",
        "icon": "lock"
    },
    {
        "title": "Assume Breach",
        "description": "Minimize blast radius, segment access, verify end-to-end encryption, and use analytics to get visibility and drive threat detection.",
        "icon": "triangle-exclamation"
    }
]

IMPLEMENTATION_STEPS = [
    {
        "step": "01",
        "title": "Cloudflare Account & Tunnel Setup",
        "description": "Create a Cloudflare Zero Trust account, install cloudflared daemon on the internal server, and authenticate it to your Cloudflare account.",
        "commands": [
            "# Install cloudflared",
            "curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb",
            "sudo dpkg -i cloudflared.deb",
            "",
            "# Authenticate cloudflared",
            "cloudflared tunnel login",
            "",
            "# Create a named tunnel",
            "cloudflared tunnel create admin-console-tunnel"
        ]
    },
    {
        "step": "02",
        "title": "Configure Tunnel & DNS",
        "description": "Create the tunnel configuration file to route traffic to your internal admin console, then create a DNS CNAME record pointing to the tunnel.",
        "commands": [
            "# ~/.cloudflared/config.yml",
            "tunnel: <YOUR_TUNNEL_ID>",
            "credentials-file: /root/.cloudflared/<TUNNEL_ID>.json",
            "",
            "ingress:",
            "  - hostname: admin.yourdomain.com",
            "    service: http://localhost:8080",
            "  - service: http_status:404",
            "",
            "# Route DNS",
            "cloudflared tunnel route dns admin-console-tunnel admin.yourdomain.com"
        ]
    },
    {
        "step": "03",
        "title": "Enable Zero Trust Access Policies",
        "description": "In the Cloudflare Zero Trust dashboard, create an Access Application for your admin console and configure identity provider (IdP) integration.",
        "commands": [
            "# Cloudflare Access Application Policy (JSON equivalent)",
            "{",
            '  "name": "Admin Console Access",',
            '  "domain": "admin.yourdomain.com",',
            '  "session_duration": "8h",',
            '  "include": [',
            '    { "email_domain": { "domain": "yourdomain.com" } }',
            "  ],",
            '  "require": [',
            '    { "mfa": { "auth_method": "totp" } }',
            "  ]",
            "}"
        ]
    },
    {
        "step": "04",
        "title": "Enforce MFA via Identity Provider",
        "description": "Integrate an IdP (Okta, Google Workspace, Azure AD) with Cloudflare Access. Configure MFA enforcement at the IdP level and require hardware key or TOTP.",
        "commands": [
            "# Example: Google Workspace OIDC Config",
            "Provider: Google Workspace",
            "Client ID: <GOOGLE_CLIENT_ID>",
            "Client Secret: <GOOGLE_CLIENT_SECRET>",
            "Auth URL: https://accounts.google.com/o/oauth2/auth",
            "Token URL: https://oauth2.googleapis.com/token",
            "",
            "# MFA Enforcement Policy",
            "Require MFA: Enabled",
            "Methods: TOTP (Authenticator App), Hardware Key (YubiKey)"
        ]
    },
    {
        "step": "05",
        "title": "Run Tunnel as a System Service",
        "description": "Install cloudflared as a system service so it starts automatically on boot, ensuring continuous protection of your admin console.",
        "commands": [
            "# Install as system service",
            "sudo cloudflared service install",
            "",
            "# Start the service",
            "sudo systemctl start cloudflared",
            "",
            "# Enable on boot",
            "sudo systemctl enable cloudflared",
            "",
            "# Verify tunnel status",
            "cloudflared tunnel info admin-console-tunnel"
        ]
    }
]

@app.route("/")
def home():
    return render_template("index.html",
                           stats=THREAT_STATS,
                           principles=ZT_PRINCIPLES,
                           current_year=datetime.now().year)

@app.route("/zero-trust")
def zero_trust():
    return render_template("zero_trust.html",
                           principles=ZT_PRINCIPLES,
                           current_year=datetime.now().year)

@app.route("/architecture")
def architecture():
    return render_template("architecture.html",
                           current_year=datetime.now().year)

@app.route("/implementation")
def implementation():
    return render_template("implementation.html",
                           steps=IMPLEMENTATION_STEPS,
                           current_year=datetime.now().year)

@app.route("/about")
def about():
    return render_template("about.html",
                           team=TEAM_MEMBERS,
                           current_year=datetime.now().year)

@app.route("/api/stats")
def api_stats():
    return jsonify(THREAT_STATS)

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("message"):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    return jsonify({"status": "success", "message": "Message received. Our team will respond within 24 hours."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
