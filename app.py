from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import smtplib
import ssl
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

# Replace these with your actual credentials
SENDER_EMAIL = "youremail@gmail.com"
SENDER_PASSWORD = "yourapppassword"
RECEIVER_EMAIL = "spreetveeraj@gmail.com"

# HTML templates (simple for demo)
login_page = '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit" value="Login">
    </form>
    {{ message }}
'''

verify_page = '''
    <h2>Enter Verification Code</h2>
    <form method="POST">
        Code: <input name="code"><br>
        <input type="submit" value="Verify">
    </form>
    {{ message }}
'''

success_page = '''
    <h2>✅ Logged in successfully!</h2>
'''

# Route: Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'preetveeraj' and request.form['password'] == '123':
            session['code'] = str(random.randint(100000, 999999))

            message = f"Subject: Your Verification Code\n\nYour code is: {session['code']}"

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login("spreetveeraj@gmail.com",  "ikkt ydai onzp xuyx")
                    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
                return redirect(url_for('verify'))
            except Exception as e:
                return render_template_string(login_page, message="Email sending failed. Check server logs.")
        else:
            return render_template_string(login_page, message="Invalid username or password.")
    return render_template_string(login_page)

# Route: Verify code
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if request.form['code'] == session.get('code'):
            return render_template_string(success_page)
        else:
            return render_template_string(verify_page, message="Incorrect code.")
    return render_template_string(verify_page)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
