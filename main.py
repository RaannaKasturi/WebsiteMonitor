import tldextract
from getStatus import getStatus
from getScreenshot import getScreenshot
from saveDataSendMail import saveDataSendMail

def cleanURL(inputURL):
    url = tldextract.extract(inputURL)
    if url.subdomain == "":
        domain = url.domain + "." + url.suffix
    else:
        domain = url.subdomain + "." + url.domain + "." + url.suffix
        URL = "http://" + domain
    return domain, URL

def main(url, email):
    domain, URL = cleanURL(url)
    code, status, webStatus, moreDetails = getStatus(URL)
    img, imgurl = getScreenshot(URL)
    email, downcount, mailStatus = saveDataSendMail(URL, email)
    return domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount, mailStatus

if __name__ == "__main__":
    works = main("https://google.com", "raannakasturi@proton.me")
    print(f"domain: {works[0]}\nURL: {works[1]}\nCode: {works[2]}\nStatus: {works[3]}\nWeb Status: {works[4]}\nMore Details: {works[5]}\nImage: {works[6]}\nImage URL: {works[7]}\nEmail: {works[8]}\nDowncount: {works[9]}\nMail Status: {works[10]}")
    print("\n ======================================================================== \n")
    notworks = main("https://arkgl.eu.org", "raannakasturi@proton.me")
    print(f"domain: {notworks[0]}\nURL: {notworks[1]}\nCode: {notworks[2]}\nStatus: {notworks[3]}\nWeb Status: {notworks[4]}\nMore Details: {notworks[5]}\nImage: {notworks[6]}\nImage URL: {notworks[7]}\nEmail: {notworks[8]}\nDowncount: {notworks[9]}\nMail Status: {notworks[10]}")