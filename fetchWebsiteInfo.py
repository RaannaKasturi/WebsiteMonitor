import getStatus
import getScreenshot
import gradio as gr

def cleanURL(URL):
    if URL.startswith("http://") or URL.startswith("https://"):
        websiteURL = URL
    else:
        websiteURL = "https://" + URL
    return websiteURL

def dispStatus(cleanedURL):
    code, status, webStatus, moreDetails = getStatus.postStatus(cleanedURL)
    return code, status, webStatus, moreDetails

def dispScreenshot(cleanedURL):
    img, imgurl = getScreenshot.getScreenshot(cleanedURL)
    return img

def fetchWebsiteInfo(URL):
    URL = URL
    if URL == "":
        img = "https://i.ibb.co/s5c9QpD/1366x768.png"
        code = "Please Enter the URL to capture the screenshot."
        status = "Please Enter the URL to capture the screenshot."
        webStatus = "Please Enter the URL to capture the screenshot."
        moreDetails = "Please Enter the URL to capture the screenshot."
        return img, code, status, webStatus, moreDetails
    else:
        cleanedURL = cleanURL(URL)
        img = dispScreenshot(cleanedURL)
        code, status, webStatus, moreDetails = dispStatus(cleanedURL)
        return img, code, status, webStatus, moreDetails

app = gr.Interface(
    fn=fetchWebsiteInfo,
    inputs = [
        gr.Textbox(label="Enter URL", placeholder="https://google.com", type="text")
    ],
    outputs = [
        gr.Image(label="Website Screenshot"),
        gr.Textbox(label="Code", type="text"),
        gr.Textbox(label="Server/Website Status", type="text"),
        gr.Textbox(label="Code Status", type="text"),
        gr.Textbox(label="More Code Status Information", type="text")
    ],
    title="Website Monitor<br><h3>by <a href='https://nayankasturi.eu.org'>Nayan Kasturi</a> aka Raanna.</h3><br><p>Checkout my <a href='https://github.com/raannakasturi'>Github</a> for more projects and contact info.</p>",
    description="This app scans the website for HTTP statuses and also screenshots it.<br> Licenced under <a href='https://github.com/RaannaKasturi/WebsiteMonitor/blob/master/LICENSE/'>MIT License</a>",
    api_name="get",
    concurrency_limit=25
)

if __name__ == "__main__":
    while True:
        if getScreenshot.checkinstallChrome() == False:
            print("App Starting...")
            app.launch()
            break
        else:
            print("OS not supported or Chrome not found in the system. Retrying...")
            True
