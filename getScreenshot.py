import os
import sys
import json
import base64
import time
import requests
import gradio as gr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import checkinstallGC

def driverSetup():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--window-size=1366,768")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Linux",
            webgl_vendor="MesaLib",
            renderer="Mesa DRI Intel(R) HD Graphics 5500",
            fix_hairline=True,
            )
    return driver

def screenshotName(url):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    url = url.replace('https://', '').replace('http://', '').replace('www.', '')
    if url.endswith('/'):
        url = url[:-1]
    return f"{url.replace('/', '')}_{timestr}.png"

def getScreenshots(driver, url):
    driver.get(url)
    ssname = screenshotName(url)
    driver.save_screenshot(ssname)
    return ssname

def saveScreenshot(url):
    driver = driverSetup()
    screenshot_file = getScreenshots(driver, url)
    driver.quit()
    return screenshot_file

def uploadandDelSS(file):
    load_dotenv()
    api = os.getenv("IMGBBAPI")
    url = os.getenv("IMGBBURL")
    filename = file
    with open(f"{filename}", "rb") as file:
        name = file.name[:-4]
        payload = {
            "key": api,
            "image": base64.b64encode(file.read()),
            "name": name,
            "expiration": "15552000"
        }
        r = requests.post(url, data=payload)
        view_url = json.loads(r.text)["data"]["display_url"]
        return view_url, view_url

def main(url):
    if url == "":
        img = "https://i.ibb.co/s5c9QpD/1366x768.png"
        imgurl = "Please Enter the URL to capture the screenshot."
        return img, imgurl
    else:
        ss = saveScreenshot(url)
        img, imgurl = uploadandDelSS(ss)
        return img, imgurl

app = gr.Interface(
    fn=main,
    inputs=[
        gr.Textbox(label="Enter URL", placeholder="https://google.com", type="text", interactive=True)
    ],
    outputs=[
        gr.Image(label="Website Screenshot"),
        gr.Textbox(label="Image URL", type="text", show_copy_button=True, interactive=False)
    ],
    title="Website Screenshot Capture<br> by <a href='https://nayankasturi.eu.org'>Nayan Kasturi</a> aka Raanna.<br> Checkout the <a href='https://github.com/raannakasturi'>Github</a> for more projects and contact info.",
    description="This app captures a screenshot of the website you enter and displays it.<br> Licenced under <a href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>cc-by-nc-sa-4.0</a>",
    api_name="capture",
    concurrency_limit=10
)

def checkSystem():
    OS = sys.platform
    if OS.startswith('linux'):
        print("Linux OS detected.")
        return "linux"
    elif OS.startswith('win32') or OS.startswith('cygwin'):
        print("Windows OS detected.")
        return "windows"
    else:
        print("Unsupported OS. We are currently supported on Windows and Linux only.")
        return "unsupported"

def checkinstallChrome():
    OS = checkSystem()
    if OS == "linux":
        return checkinstallGC.checkGC("linux")
    elif OS == "windows":
        return checkinstallGC.checkGC("windows")
    else:
        print("Can't check for Chrome installation or install Chrome. Exiting..")
        return False

if __name__ == "__main__":
    while True:
        if checkinstallChrome() == False:
            print("App Starting...")
            app.launch()
            break
        else:
            print("OS not supported or Chrome not found in the system. Retrying...")
            True