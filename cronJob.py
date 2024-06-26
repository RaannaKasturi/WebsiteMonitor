from datetime import datetime 
import time
import pytz
import schedule
from remove_fetchWebsiteInfo import fetchWebsiteInfo

def job():
    data = fetchWebsiteInfo("https://google.com")
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    currtime = datetime_ist.strftime('%H:%M:%S %Z%z')
    with open("log.txt", "a") as f:
        f.write(f"{str(currtime)}\t")
        f.write(f"Img Link: {data[0]}\t")
        f.write(f"Code: {data[1]}\t")
        f.write(f"Status: {data[2]}\t")
        f.write(f"Web Status: {data[3]}\t")
        f.write(f"More Details: {data[4]}\n")

schedule.every(3).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)