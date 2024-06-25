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

# ID - Domain - Email - Status - DownCount
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
  getData = f"select * from UserData where Domain = '{domain}';"
  data = cursor.execute(getData)
  conn.commit()
  conn.close()
  return data

def getData(EMAIL, URL, downcount):
    cleanedURL = cleanURL(URL)
    data = dispStatus(cleanedURL)
    if data[0] == "200":
        status = "Up"
        downcount = 0
    else:
        status = "Down"
        downcount += 1
    domainData = tldextract.extract(cleanedURL)
    domain = domainData.subdomain+"."+domainData.domain+"."+domainData.suffix
    email = EMAIL
    return domain, email, status, downcount

if __name__ == "__main__":
    inputURL = input("Enter the URL to monitor: ")
    email = input("Enter your email address: ")
    domain, email, status, downcount = getData(email, inputURL, 0)
    try:
        # Try to get existing data
        DOMAIN, EMAIL, STATUS, DOWNCOUNT = get(domain)
        if DOMAIN is not None:  # Check if data was found
            # Update data using retrieved downcount
            domain, email, status, downcount = getData(inputURL, email, DOWNCOUNT)
            insert(domain, email, status, downcount)
            get(domain)  # Print updated data
        else:
            # No existing data, insert new entry
            insert(domain, email, status, 0)
            get(domain)
    except psycopg2.errors.DataException as e:
        # Handle other database errors
        print(f"Database error: {e}")
    except:
        insert(domain, email, status, 0)
        get(domain)
    finally:
        print("Data inserted successfully")
        get(domain)
