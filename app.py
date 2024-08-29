from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Configurations for Gmail SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USER = 'your_email@gmail.com'
GMAIL_PASSWORD = 'your_email_password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'subscribe' in request.form:
            email = request.form.get('email')
            
            if not email:
                flash('Please enter a valid email address.', 'error')
            else:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = GMAIL_USER
                    msg['To'] = GMAIL_USER
                    msg['Subject'] = 'New Newsletter Subscription'
                    
                    body = f'New subscription from: {email}'
                    msg.attach(MIMEText(body, 'plain'))
                    
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(GMAIL_USER, GMAIL_PASSWORD)
                        server.send_message(msg)

                    flash('Subscription successful! Thank you for subscribing.', 'success')
                except Exception as e:
                    flash(f'An error occurred: {e}', 'error')

        elif 'contact' in request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = 'fitmeonline@gmail.com'
            msg['Subject'] = f"Contact Form Submission: {subject}"
            
            body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                flash('Your message has been sent. Thank you!', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
