import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
from fetchWebsiteInfo import dispStatus
import tldextract
import smtplib
from email.mime.text import MIMEText
import ssl

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_DATABASE_PORT')
endpoint_id = os.getenv('ENDPOINT_ID')
sender_email = os.getenv('EMAIL_ADDRESS')
sender_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')

databaseConn = f"postgresql://{user}:{password}@{host}:{port}/{database}?options=endpoint%3D{endpoint_id}"

def insert(domain, email, status, downcount):
    try:
        conn = psycopg2.connect(databaseConn)
        cursor = conn.cursor()
        insertData = """
            INSERT INTO USERDATA (DOMAIN, EMAIL, STATUS, DOWNCOUNT)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insertData, (domain, email, status, downcount))
        conn.commit()
        print(f"Data for {domain} inserted successfully.")
    except Exception as e:
        print(f"Error inserting data for {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

def get(domain):
    try:
        conn = psycopg2.connect(databaseConn)
        cursor = conn.cursor()
        getData = """
            SELECT STATUS, DOWNCOUNT FROM USERDATA WHERE DOMAIN = %s;
        """
        cursor.execute(getData, (domain,))
        existing_data = cursor.fetchone()
        if existing_data:
            return existing_data[1]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving data for {domain}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update(domain, status, downcount):
    try:
        conn = psycopg2.connect(databaseConn)
        cursor = conn.cursor()
        updateData = """
            UPDATE USERDATA SET STATUS = %s, DOWNCOUNT = %s WHERE DOMAIN = %s;
        """
        cursor.execute(updateData, (status, downcount, domain))
        conn.commit()
        print(f"Data for {domain} updated successfully.")
    except Exception as e:
        print(f"Error updating data for {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

def getData(EMAIL, URL, downcount):
    data = dispStatus(URL)
    if data[0].startswith("2") or data[0].startswith("3"):
        status = "Up"
        downcount = 0
    else:
        status = "Down"
        downcount += 1
    domainData = tldextract.extract(URL)
    if domainData.subdomain == "":
        domain = domainData.domain + "." + domainData.suffix
    else:
        domain = domainData.subdomain + "." + domainData.domain + "." + domainData.suffix
    email = EMAIL
    return domain, email, status, downcount

def saveDataSendMail(URL, email):
    domain, email, status, downcount = getData(email, URL, 0)
    existing_downcount = get(domain)

    if existing_downcount is None:
        existing_downcount = 0
        if status == "Up":
            downcount = 0
        else:
            downcount = existing_downcount + 1
            sendMail(email, domain, status)
        insert(domain, email, status, downcount)
    else:
        if status == "Up":
            downcount = 0
        else:
            downcount = existing_downcount + 1
            sendMail(email, domain, status)
        update(domain, status, downcount)
    print(f"{domain} is currently {status}")
    return email, downcount,

def sendMail(recipient_email, website_domain, status):
    """Sends an email notification to the user when the website is down."""
    subject = f"Website Alert: {website_domain} is currently {status}"
    body = f"The website {website_domain} is currently unavailable.\nPlease check it as soon as possible.\nIf you think this is a mistake, Contact Us."

    message = MIMEText(body, 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            return f"Sent email notification for {website_domain} to {recipient_email}"
    except Exception as e:
        return f"Error sending email: {e}"

