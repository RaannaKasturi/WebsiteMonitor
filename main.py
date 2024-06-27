import tldextract
from getStatus import getStatus
from getScreenshot import getScreenshot
from saveDataSendMail import saveDataSendMail
import subprocess
import sys

def cleanURL(inputURL):
    url = tldextract.extract(inputURL)
    if url.subdomain == "":
        domain = url.domain + "." + url.suffix
        URL = "https://" + domain
    else:
        domain = url.subdomain + "." + url.domain + "." + url.suffix
        URL = "https://" + domain
    return domain, URL

def getData(url, email):
    domain, URL = cleanURL(url)
    code, status, webStatus, moreDetails = getStatus(URL)
    if code.startswith("2"):
        img, imgurl = getScreenshot(URL)
    else:
        img = "1366-768.png"
        imgurl = "Website is down. No screenshot available."
    email, downcount = saveDataSendMail(URL, email)
    return domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount

def installGC():
    OS = sys.platform
    if OS == 'linux':
        subprocess.run(['apt-get', 'update'])
        subprocess.run(['apt-get', 'install', '-y', 'wget', 'unzip'])
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
        subprocess.run(['apt-get', 'install', '-y', './google-chrome-stable_current_amd64.deb'])
        subprocess.run(['rm', 'google-chrome-stable_current_amd64.deb'])
        subprocess.run(['apt-get', 'clean'])
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'wget', 'unzip'])
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', './google-chrome-stable_current_amd64.deb'])
        subprocess.run(['sudo', 'rm', 'google-chrome-stable_current_amd64.deb'])
        subprocess.run(['sudo', 'apt-get', 'clean'])
    else:
        subprocess.run(['powershell', '-command', 'winget', 'install', 'Google.Chrome', '--force'])