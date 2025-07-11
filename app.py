from flask import Flask, request, render_template
import re
import dns.resolver
import smtplib

app = Flask(__name__)

def is_valid_format(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def has_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except:
        return False

def check_smtp(email):
    domain = email.split('@')[1]
    try:
        mx_record = dns.resolver.resolve(domain, 'MX')[0].exchange.to_text()
        server = smtplib.SMTP(timeout=5)
        server.connect(mx_record)
        server.helo()
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        email = request.form['email']
        if not is_valid_format(email):
            result = f"❌ Invalid format: {email}"
        else:
            domain = email.split('@')[1]
            if not has_mx_record(domain):
                result = f"❌ Domain has no MX record: {domain}"
            else:
                if check_smtp(email):
                    result = f"✅ Email is likely deliverable: {email}"
                else:
                    result = f"⚠️ Format and MX are valid, but SMTP check failed (maybe temporary issue)"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
