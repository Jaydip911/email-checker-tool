from flask import Flask, request, jsonify
import dns.resolver
import re
import json

app = Flask(__name__)

DISPOSABLE_DOMAINS = set([
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "tempmail.com", "yopmail.com", "trashmail.com", "sharklasers.com"
])

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def has_mx(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except:
        return False

@app.route("/api/check", methods=["POST"])
def check_email():
    data = request.get_json()
    emails = data.get("emails", [])

    results = []
    for email in emails:
        email = email.strip()
        status = {"email": email}

        if not EMAIL_REGEX.match(email):
            status["valid"] = False
            status["reason"] = "Invalid Format"
        else:
            domain = email.split("@")[1]
            if domain.lower() in DISPOSABLE_DOMAINS:
                status["valid"] = False
                status["reason"] = "Disposable Email"
            elif not has_mx(domain):
                status["valid"] = False
                status["reason"] = "No MX Record"
            else:
                status["valid"] = True
                status["reason"] = "Valid Email"

        results.append(status)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
