import random, os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, otp: str):
    subject = "Your OTP for B2B Authentication"
    body = f"Your OTP is: {otp}. It will expire in 10 minutes."
    
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject=subject,
        plain_text_content=body)
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"SendGrid response code: {response.status_code}")
        return response.status_code == 202  # SendGrid returns 202 on success
    except Exception as e:
        print(f"Error sending email: {e}")
        return False