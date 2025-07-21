from flask import Flask, render_template, request, jsonify
import dns.resolver
import smtplib
import socket

app = Flask(__name__)

def smtp_check(email):
    domain = email.split('@')[-1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('check@example.com')
        code, message = server.rcpt(email)
        server.quit()
        if code == 250:
            return "Valid"
        elif code == 550:
            return "Invalid"
        else:
            return "Unknown"
    except Exception:
        return "Invalid"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    emails = data.get("emails", [])
    results = [{"email": email, "status": smtp_check(email)} for email in emails]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
