import psycopg2
from dotenv import load_dotenv
import os
from fetchWebsiteInfo import cleanURL, dispStatus
import tldextract

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')


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

    existing_data = get(domain)

    if existing_data is None:  # Check if domain exists
        # Insert new entry
        insert(domain, email, status, downcount)
        print(f"Website for {domain} is {status}")
    else:
        # Update existing data based on website status
        existing_downcount = existing_data
        if status == "Up":
            downcount = 0  # Reset downcount if website is Up
        else:
            downcount = existing_downcount + 1  # Increase downcount if Down
        update(domain, status, downcount)
        print(f"Website for {domain} is currently {status}")

if __name__ == "__main__":
    saveData()
