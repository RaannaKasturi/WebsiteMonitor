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
        URL = "http://" + domain
    else:
        domain = url.subdomain + "." + url.domain + "." + url.suffix
        URL = "http://" + domain
    return domain, URL

def getData(url, email):
    domain, URL = cleanURL(url)
    code, status, webStatus, moreDetails = getStatus(URL)
    img, imgurl = getScreenshot(URL)
    email, downcount = saveDataSendMail(URL, email)
    return domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount

def installGC():
    if sys.platform == 'linix':
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