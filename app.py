from flask import Flask, request, jsonify, render_template
import re
import dns.resolver

app = Flask(__name__)

def validate_email_syntax(email):
    regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(regex, email)

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_email():
    data = request.json
    emails = data.get("emails", [])
    results = []

    for email in emails:
        email = email.strip()
        is_valid = bool(validate_email_syntax(email))
        domain = email.split("@")[-1] if "@" in email else ""
        mx_valid = has_mx_record(domain) if is_valid else False

        results.append({
            "email": email,
            "syntax": is_valid,
            "mx": mx_valid
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
