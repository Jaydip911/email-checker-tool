from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/check", methods=["POST"])
def check_emails():
    data = request.get_json()
    emails = data.get("emails", [])

    # Placeholder validation logic
    results = []
    for email in emails:
        result = {
            "email": email,
            "mx": "@gmail.com" in email or "@yahoo.com" in email,
            "disposable": "tempmail" in email or "mailinator" in email
        }
        results.append(result)

    return jsonify({"results": results})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets this environment variable
    app.run(host="0.0.0.0", port=port)
