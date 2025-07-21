from flask import Flask, render_template, request, jsonify
import smtplib
import dns.resolver
import re

app = Flask(__name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def check_email_smtp(email):
    domain = email.split('@')[-1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    emails = request.json.get('emails', [])
    results = []
    for email in emails:
        email = email.strip()
        if not EMAIL_REGEX.match(email):
            result = {'email': email, 'status': 'Invalid Format'}
        else:
            is_valid = check_email_smtp(email)
            result = {'email': email, 'status': 'Valid' if is_valid else 'Invalid'}
        results.append(result)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
