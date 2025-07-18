from flask import Flask, request, jsonify
import dns.resolver
import re

app = Flask(__name__)

# Sample list of disposable email domains (you can expand this)
DISPOSABLE_DOMAINS = set([
    "mailinator.com", "10minutemail.com", "guerrillamail.com", "temp-mail.org",
    "trashmail.com", "dispostable.com", "yopmail.com"
])

# Simple regex check
def is_valid_syntax(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email)

# MX Record check
def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

# Disposable domain check
def is_disposable(email):
    domain = email.split('@')[-1].lower()
    return domain in DISPOSABLE_DOMAINS

@app.route('/api/check', methods=['POST'])
def check_email():
    data = request.get_json()
    emails = data.get("emails", [])
    
    results = []
    for email in emails:
        email = email.strip()
        if not is_valid_syntax(email):
            results.append({"email": email, "status": "Invalid Syntax"})
            continue

        domain = email.split('@')[-1]
        if is_disposable(email):
            results.append({"email": email, "status": "Disposable"})
        elif has_mx_record(domain):
            results.append({"email": email, "status": "Valid (MX found)"})
        else:
            results.append({"email": email, "status": "No MX Record"})

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
