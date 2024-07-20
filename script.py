import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os
import re
from tqdm import tqdm

visited_urls = set()
url_list_file = 'list_url.txt'

def fetch_content(url):
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

def crawl(url, base_url, depth=0, max_depth=5):
    if url in visited_urls or depth > max_depth:
        print(f"Skipping URL (already visited or max depth reached): {url}")
        return
    print(f"Crawling URL: {url}, Depth: {depth}")
    visited_urls.add(url)
    save_url_to_file(url)

    html_content = fetch_content(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            next_url = urljoin(base_url, link['href'])
            if is_valid_url(next_url, base_url):
                crawl(next_url, base_url, depth + 1, max_depth)
#                time.sleep(1)  # Respectful crawling

def html_to_markdown(html_content):
    markdown_content = md(html_content)
    return re.sub(r'\n\s*\n', '\n\n', markdown_content)  # Remove excessive blank lines

def save_markdown(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {filename}")

def extract_main_content(soup):
    main_content_selectors = [
        {'id': re.compile('.*content.*', re.IGNORECASE)},
        {'class': re.compile('.*content.*', re.IGNORECASE)},
        {'class': 'post-content'},
        {'class': 'entry-content'},
        {'class': 'article-content'},
        {'class': 'article-body'},
        {'class': 'post-body'},
        {'class': 'entry-body'},
        {'class': 'main-content'},
        {'class': 'story-body'},
        {'class': 'post'},
        {'class': 'entry'},
        {'class': 'content-area'},
        {'role': 'main'}
    ]

    for selector in main_content_selectors:
        main_content = soup.find(attrs=selector)
        if main_content:
            return main_content

    # If no specific main content found, try to find the largest content block
    all_divs = soup.find_all('div')
    max_div = max(all_divs, key=lambda div: len(div.text), default=None)
    return max_div

def process_url_list(file_path):
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for index, url in enumerate(tqdm(urls, desc="Processing URLs", unit="url")):
        url = url.strip()
        if not url:
            continue
        print(f"Processing URL {index + 1}/{len(urls)}: {url}")
        
        html_content = fetch_content(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            main_content = extract_main_content(soup)
            if main_content:
                markdown_content = html_to_markdown(str(main_content))
                
                # Generate a safe filename based on the URL path
                parsed_url = urlparse(url)
                path_parts = [part for part in parsed_url.path.split('/') if part]
                filename = os.path.join(parsed_url.netloc, '_'.join(path_parts) + '.md')
                
                save_markdown(markdown_content, filename)
            else:
                print(f"No main content found for URL: {url}")
        else:
            print(f"Failed to fetch content for URL: {url}")

def main():
    start_url = input("Enter the URL to start crawling: ")
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))

    print(f"Starting crawling at {start_url}")
    crawl(start_url, base_url)
    print("Crawling complete.")
    
    # Start processing the URL list to convert content to Markdown
    print("Starting to process URL list for Markdown conversion.")
    process_url_list(url_list_file)
    print("Markdown conversion complete.")

if __name__ == "__main__":
    main()
