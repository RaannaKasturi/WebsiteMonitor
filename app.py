import gradio as gr
from main import getData, installGC

def run(URL, email):
    domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount = getData(URL, email)
    return domain, URL, code, status, webStatus, moreDetails, img, imgurl, email, downcount

app = gr.Interface(
    fn=run,
    inputs=[
        gr.Textbox(label="Enter URL", placeholder="https://google.com", type="text", interactive=True),
        gr.Textbox(label="Enter Email", placeholder="example@gmail.com", type="email", interactive=True)
    ],
    outputs=[
        gr.Textbox(label="Domain", type="text", interactive=False),
        gr.Textbox(label="URL", type="text", interactive=False),
        gr.Textbox(label="Code", type="text", interactive=False),
        gr.Textbox(label="Status", type="text", interactive=False),
        gr.Textbox(label="Web Status", type="text", interactive=False),
        gr.Textbox(label="More Details", type="text", interactive=False),
        gr.Image(label="Website Screenshot"),
        gr.Textbox(label="Screenshot URL/Error", type="text", interactive=False),
        gr.Textbox(label="Email", type="email", interactive=False),
        gr.Textbox(label="Download Count", type="text", interactive=False),
    ],
    title="Website Monitor<br> by <a href='https://nayankasturi.eu.org'>Nayan Kasturi</a> aka Raanna.<br> Checkout the <a href='https://github.com/raannakasturi'>Github</a> for more projects and contact info.",
    description="This app captures website status and its screenshot and displays it, along with sending mail to the person, in case website is down.",
    api_name="get",
    concurrency_limit=10
)

if __name__ == "__main__":
    installGC()
    app.launch()