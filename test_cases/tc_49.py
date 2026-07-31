# Clean web scraping code
import urllib.request

def fetch(url):
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

pages = ["https://example.com", "https://example.org"]
