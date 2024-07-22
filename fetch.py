import requests
import os
from urllib.parse import urlparse
from tqdm import tqdm
from dotenv import load_dotenv
import json

# โหลดข้อมูลจากไฟล์ .env
load_dotenv()
auth_token = os.getenv("JINA_AUTH_TOKEN")

status_file = 'fetch_status.json'

def fetch_content_with_jina(url):
    try:
        print(f"Fetching URL with Jina: {url}")
        jina_url = f"https://r.jina.ai/{url}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url} with Jina: {e}")
        return None

def save_markdown(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    file_size = os.path.getsize(filename)
    print(f"Content saved to {filename} with size {file_size} bytes")

def save_status(status):
    with open(status_file, 'w', encoding='utf-8') as file:
        json.dump(status, file)
    print(f"Status saved to {status_file}")

def load_status():
    if os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def process_url_list(file_path):
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return

    status = load_status()
    start_index = 0
    if status:
        start_index = status['current_index']
        print(f"Resuming from index {start_index}")

    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for index, url in enumerate(tqdm(urls[start_index:], initial=start_index, total=len(urls), desc="Processing URLs", unit="url")):
        url = url.strip()
        if not url:
            continue
        print(f"Processing URL {index + 1}/{len(urls)}: {url}")

        content = fetch_content_with_jina(url)
        if content:
            parsed_url = urlparse(url)
            path_parts = [part for part in parsed_url.path.split('/') if part]
            filename = os.path.join(parsed_url.netloc, '_'.join(path_parts) + '.md')

            save_markdown(content, filename)
        else:
            print(f"Failed to fetch content for URL: {url}")

        save_status({'current_index': index + 1})

def main():
    url_list_file = 'list_url.txt'
    print("Starting to process URL list for Markdown conversion.")
    process_url_list(url_list_file)
    print("Markdown conversion complete.")
    if os.path.exists(status_file):
        os.remove(status_file)
    print("Status file removed.")

if __name__ == "__main__":
    main()

