import requests
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

visited_urls = set()
url_list_file = 'list_url.txt'
status_file = 'crawl_status.json'

def fetch_html(url):
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def is_valid_url(url, base_url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == urlparse(base_url).netloc

def save_url_to_file(url):
    with open(url_list_file, 'a', encoding='utf-8') as file:
        file.write(url + '\n')
    print(f"URL saved to {url_list_file}: {url}")

def save_status(status):
    with open(status_file, 'w', encoding='utf-8') as file:
        json.dump(status, file)
    print(f"Status saved to {status_file}")

def load_status():
    if os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def crawl(url, base_url, depth=0, max_depth=5):
    if url in visited_urls or depth > max_depth:
        print(f"Skipping URL (already visited or max depth reached): {url}")
        return
    print(f"Crawling URL: {url}, Depth: {depth}")
    visited_urls.add(url)
    save_url_to_file(url)
    save_status({'current_url': url, 'depth': depth})

    html_content = fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            next_url = urljoin(base_url, link['href'])
            if is_valid_url(next_url, base_url):
                try:
                    crawl(next_url, base_url, depth + 1, max_depth)
                except Exception as e:
                    print(f"Error during crawling {next_url}: {e}")
                    break

def main():
    status = load_status()
    if status:
        start_url = status['current_url']
        depth = status['depth']
        print(f"Resuming from {start_url} at depth {depth}")
    else:
        start_url = input("Enter the URL to start crawling: ")
        depth = 0

    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))
    print(f"Starting crawling at {start_url}")

    try:
        crawl(start_url, base_url, depth)
    except Exception as e:
        print(f"Error during crawling: {e}")
    
    print("Crawling complete.")
    if os.path.exists(status_file):
        os.remove(status_file)
    print("Status file removed.")

if __name__ == "__main__":
    main()

