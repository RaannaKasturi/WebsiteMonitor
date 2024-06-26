import gradio as gr
from main import getData, installGC

def run(URL, email):
    domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount = getData(URL, email)
    return domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount

app = gr.Interface(
    fn=run,
    inputs=[
        gr.Textbox(label="Enter URL", placeholder="https://google.com", type="text", interactive=True),
        gr.Textbox(label="Enter Email", placeholder="raannakasturi@proton.me", type="text", interactive=True)
    ],
    outputs=[
        gr.Textbox(label="Domain", type="text", interactive=False),
        gr.Textbox(label="URL", type="text", interactive=False),
        gr.Textbox(label="Code", type="text", interactive=False),
        gr.Textbox(label="Status", type="text", interactive=False),
        gr.Textbox(label="Web Status", type="text", interactive=False),
        gr.Textbox(label="More Details", type="text", interactive=False),
        gr.Image(label="Website Screenshot"),        
        gr.Textbox(label="Email", type="text", interactive=False),
        gr.Textbox(label="Download Count", type="text", interactive=False),
    ],
    title="Website Screenshot Capture<br> by <a href='https://nayankasturi.eu.org'>Nayan Kasturi</a> aka Raanna.<br> Checkout the <a href='https://github.com/raannakasturi'>Github</a> for more projects and contact info.",
    description="This app captures a screenshot of the website you enter and displays it.<br> Licenced under <a href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>cc-by-nc-sa-4.0</a>",
    api_name="capture",
    concurrency_limit=10
)

if __name__ == "__main__":
    #installGC()
    app.launch()