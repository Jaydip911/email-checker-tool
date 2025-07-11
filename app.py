from flask import Flask, render_template, request
import dns.resolver
import socket

app = Flask(__name__)

def verify_email(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text()
        # Try connecting to the mail server
        socket.create_connection((mx_record, 25), timeout=5)
        return True
    except Exception:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    email = ''
    if request.method == 'POST':
        email = request.form['email']
        result = verify_email(email)
    return render_template('index.html', result=result, email=email)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
