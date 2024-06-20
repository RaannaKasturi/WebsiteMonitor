import base64
import json
import os
import time
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import gradio as gr
from getStatus import run  # Assuming this module contains the run function

# Function to setup WebDriver for capturing screenshot
def driverSetup():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Linux",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

# Function to generate screenshot filename based on URL
def screenshotName(url):
    if url.startswith('https://'):
        url = url.replace('https://', '')
    elif url.startswith('http://'):
        url = url.replace('http://', '')
    elif url.startswith('http://www.'):
        url = url.replace('http://www.', '')
    elif url.startswith('https://www.'):
        url = url.replace('https://www.', '')
    else:
        url = url
    if url.endswith('/'):
        url = url[:-1]
    else:
        url = url
    ssname = f"SS_{url.replace('/', '')}.png"
    return ssname

# Function to capture screenshot and return filename
def getScreenshots(driver, url):
    driver.get(url)
    ssname = screenshotName(url)
    time.sleep(3)
    driver.save_screenshot(ssname)
    return ssname

# Function to save screenshot using WebDriver
def saveScreenshot(url):
    driver = driverSetup()
    screenshot_file = getScreenshots(driver, url)
    driver.quit()
    return screenshot_file

# Function to upload screenshot to ImgBB and return display URL
def uploadandDelSS(file):
    load_dotenv()
    api = os.getenv("IMGBBAPI")
    url = os.getenv("IMGBBURL")
    filename = file
    with open(f"{filename}", "rb") as file:
        payload = {
            "key": api,
            "image": base64.b64encode(file.read()),
            "name": f"SS_{filename}",
            "expiration": "15552000"
        }
        r = requests.post(url, data= payload)
        view_url=(json.loads(r.text)["data"]["display_url"])
        file.close()
        os.remove(filename)
        return view_url, view_url

# Function to check website status and return status information
def getStatus(code):
    with open('status.json', 'r') as file:
        data = json.load(file)
        try:
            if code.startswith("2"):
                status = data['WebStatus']['Online']['SuccessfulConnection'][code]
                webstatus = "Online"
                morestatus = f"The website is currently functioning optimally and delivering content successfully."
                return code, webstatus, status, morestatus
            elif code.startswith("3"):
                status = data['WebStatus']['Online']['Redirection'][code]
                webstatus = "Online"
                morestatus = f"The website is employing a redirection mechanism to direct users to a different URL (Redirection code: {code})."
                return code, webstatus, status, morestatus
            elif code.startswith("4"):
                status = data['WebStatus']['Offline']['ClientError'][code]
                webstatus = "Offline. Client-side Error or Unauthorization Error or Authentication Error."
                morestatus = f"Website is offline due to a client-side error (Client Error code: {code}). This could be caused by an invalid request or issue with your browser."
                return code, webstatus, status, morestatus
            elif code.startswith("5"):
                status = data['WebStatus']['Offline']['ServerError'][code]
                webstatus = "Offline"
                morestatus = f"Website is offline due to a server-side error (Server Error code: {code}). This indicates an issue with the website itself or its infrastructure."
                return code, webstatus, status, morestatus
            else:
                return "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance."
        except KeyError:
            return "abc.", "def.", "ghi.", "jkl."

# Function to run the combined functionality
def websitemonitor(url, user_agent_choice):
    try:
        # Check website status
        web_response = requests.get(url, user_agent_choice, timeout=5)
        web_status = str(web_response.status_code)
        code, webstatus, status, morestatus = getStatus(web_status)

        # Capture screenshot
        screenshot_file = saveScreenshot(url)

        # Upload screenshot and get display URL
        img, imgurl = uploadandDelSS(screenshot_file)

        return code, webstatus, status, morestatus, img

    except requests.RequestException as e:
        error = f"An error occurred while fetching website status: {e}"
        return error, error, error, error, None
    except Exception as e:
        error = f"An unexpected error occurred: {e}"
        return error, error, error, error, None

# Create a Gradio interface
app = gr.Interface(
    fn=websitemonitor,
    inputs = [
        gr.Textbox(label="Enter URL", placeholder="https://google.com", type="text"),
        gr.Radio(["Your Browser Headers", "Our Server Headers"], label="Select User Agent")
    ],
    outputs = [
        gr.Textbox(label="Code", type="text"),
        gr.Textbox(label="Server/Website Status", type="text"),
        gr.Textbox(label="Code Status", type="text"),
        gr.Textbox(label="More Code Status Information", type="text"),
        gr.Image(label="Website Screenshot", type="filepath")
    ],
    title="Website Monitor with Screenshot Capture",
    description="This app checks the status of a website and captures its screenshot.",
    api_name="monitor",
)

# Launch the Gradio interface
if __name__ == "__main__":
    app.launch()
