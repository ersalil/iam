
import smtplib
from email.message import EmailMessage

def send_email(subject: str, body: str, to_email: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "youremail@example.com"  # This should be replaced with your actual email
    msg['To'] = to_email
    
    server = smtplib.SMTP('smtp.example.com')  # Replace with your SMTP server
    server.send_message(msg)
    server.quit()
