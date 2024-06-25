import psycopg2
from dotenv import load_dotenv
import os
from fetchWebsiteInfo import cleanURL, dispStatus
import tldextract
import smtplib
from email.mime.text import MIMEText
import ssl

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
sender_email = os.getenv('EMAIL_ADDRESS')
sender_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')

def insert(domain, email, status, downcount):
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host
    )
    cursor = conn.cursor()
    insertData = f"INSERT INTO USERDATA (DOMAIN, EMAIL, STATUS, DOWNCOUNT) VALUES ('{domain}', '{email}', '{status}', {downcount});"
    cursor.execute(insertData)
    conn.commit()
    conn.close()


def get(domain):
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host
    )
    cursor = conn.cursor()
    getData = f"select STATUS, DOWNCOUNT from UserData where Domain = '{domain}';"
    data = cursor.execute(getData)
    existing_data = cursor.fetchone()  # Fetch status and downcount
    existing_data = existing_data[1]  # Extract downcount from the tuple
    conn.commit()
    conn.close()
    return existing_data


def update(domain, status, downcount):
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host
    )
    cursor = conn.cursor()
    updateData = f"UPDATE USERDATA SET STATUS = '{status}', DOWNCOUNT = {downcount} WHERE DOMAIN = '{domain}';"
    cursor.execute(updateData)
    conn.commit()
    conn.close()


def getData(EMAIL, URL, downcount):
    cleanedURL = cleanURL(URL)
    data = dispStatus(cleanedURL)
    if data[0].startswith == "2" or data[0].startswith == "3":
        status = "Up"
        downcount = 0
    else:
        status = "Down"
        downcount += 1
    domainData = tldextract.extract(cleanedURL)
    domain = domainData.subdomain + "." + domainData.domain + "." + domainData.suffix
    email = EMAIL
    return domain, email, status, downcount

def saveData():
    inputURL = input("Enter the URL to monitor: ")
    email = input("Enter your email address: ")

    domain, email, status, downcount = getData(email, inputURL, 0)
    downcount = int(downcount)
    existing_data: int = get(domain)

    if existing_data is None:  # Check if domain exists
        # Insert new entry
        insert(domain, email, status, downcount)
        if status == "Up":
            downcount = 0  # Reset downcount if website is Up
        else:
            downcount = existing_downcount + 1  # Increase downcount if Down
            insert(domain, email, status, downcount)
            sendMail(email, domain, status)
        print(f"{domain} is currently {status}")
    else:
        # Update existing data based on website status
        existing_downcount = existing_data
        if status == "Up":
            downcount = 0  # Reset downcount if website is Up
        else:
            downcount = int(existing_downcount) + 1  # Increase downcount if Down
            sendMail(email, domain, status)
        update(domain, status, downcount)
        print(f"{domain} is currently {status}")

def sendMail(recipient_email, website_domain, status):
    """Sends an email notification to the user when the website is down."""

    subject = f"Website Alert: {website_domain} is currently {status}"
    body = f"The website {website_domain} is currently unavailable.\nPlease check it as soon as possible.\nIf you think this is a mistake, Contact Us."

    message = MIMEText(body, 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Sent email notification for {website_domain} to {recipient_email}")

if __name__ == "__main__":
    saveData()
