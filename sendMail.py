import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


# Load environment variables (including email details)
load_dotenv()
sender_email = os.getenv('EMAIL_ADDRESS')
sender_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')


def sendMail(recipient_email, website_domain, status):
  """Sends an email notification to the user when the website is down."""

  subject = f"Website Alert: {website_domain} is currently {status}"
  body = f"The website {website_domain} is currently unavailable.\nPlease check it as soon as possible.\nIf you think this is a mistake, Contact Us."

  message = MIMEText(body, 'plain')
  message['Subject'] = subject
  message['From'] = sender_email
  message['To'] = recipient_email

  with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    print(f"Sent email notification for {website_domain} to {recipient_email}")