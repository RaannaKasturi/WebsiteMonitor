from bs4 import BeautifulSoup
from celery import Celery
from fastapi import requests
from celeryconfig import broker_url, result_backend

celery_app = Celery('tasks', broker=broker_url, backend=result_backend)
celery_app.config_from_object('celeryconfig')

@celery_app.task
def process_topic(topic):
    search_html = fetch_search_results(topic)
    links = parse_results(search_html)
    
    full_text = ""
    for link in links:
        webpage_html = scrape_webpage(link)
        text = extract_text(webpage_html)
        full_text += text + " "
    
    summary = summarize_text(full_text)
    return summary

def fetch_search_results(query, num_results=5):
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    return response.text

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    result_divs = soup.find_all('div', class_='g')
    links = []
    for div in result_divs:
        a_tag = div.find('a')
        if a_tag and a_tag['href']:
            links.append(a_tag['href'])
    return links

def scrape_webpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    return response.text

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    page_text = ' '.join([para.get_text() for para in paragraphs])
    return page_text

def summarize_text(text, max_sentences=10):
    sentences = text.split('. ')
    if len(sentences) <= max_sentences:
        return text
    summary = '. '.join(sentences[:max_sentences]) + '.'
    return summary
