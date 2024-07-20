import requests
import os
from urllib.parse import urljoin, urlparse
import re
from tqdm import tqdm
from dotenv import load_dotenv

# โหลดข้อมูลจากไฟล์ .env
load_dotenv()
auth_token = os.getenv("JINA_AUTH_TOKEN")

# เซ็ตที่เก็บ URL ที่เคยเข้าเยี่ยมชมแล้ว
visited_urls = set()

# ชื่อไฟล์ที่เก็บรายการ URL
url_list_file = 'list_url.txt'

# ฟังก์ชันสำหรับดึงเนื้อหาจาก URL โดยใช้ Jina AI Reader
def fetch_content_with_jina(url):
    try:
        print(f"Fetching URL with Jina: {url}")
        # สร้าง URL สำหรับ Jina AI Reader
        jina_url = f"https://r.jina.ai/{url}"
        headers = {
            "Authorization": f"Bearer {auth_token}"  # เพิ่ม Authorization header
        }
        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url} with Jina: {e}")
        return None

# ฟังก์ชันตรวจสอบว่า URL นั้นเป็น URL ที่อยู่ใน domain เดียวกันหรือไม่
def is_valid_url(url, base_url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == urlparse(base_url).netloc

# ฟังก์ชันบันทึก URL ลงในไฟล์
def save_url_to_file(url):
    with open(url_list_file, 'a', encoding='utf-8') as file:
        file.write(url + '\n')
    print(f"URL saved to {url_list_file}: {url}")

# ฟังก์ชันการ crawl URL
def crawl(url, base_url, depth=0, max_depth=5):
    if url in visited_urls or depth > max_depth:
        print(f"Skipping URL (already visited or max depth reached): {url}")
        return
    print(f"Crawling URL: {url}, Depth: {depth}")
    visited_urls.add(url)
    save_url_to_file(url)

    content = fetch_content_with_jina(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            next_url = urljoin(base_url, link['href'])
            if is_valid_url(next_url, base_url):
                crawl(next_url, base_url, depth + 1, max_depth)

# ฟังก์ชันบันทึกเนื้อหาเป็นไฟล์ Markdown
def save_markdown(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    file_size = os.path.getsize(filename)
    print(f"Content saved to {filename} with size {file_size} bytes")

# ฟังก์ชันประมวลผลรายการ URL ที่เก็บไว้ในไฟล์
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

        content = fetch_content_with_jina(url)
        if content:
            parsed_url = urlparse(url)
            path_parts = [part for part in parsed_url.path.split('/') if part]
            filename = os.path.join(parsed_url.netloc, '_'.join(path_parts) + '.md')

            save_markdown(content, filename)
        else:
            print(f"Failed to fetch content for URL: {url}")

# ฟังก์ชันหลักในการควบคุมการทำงานทั้งหมด
def main():
    if os.path.exists(url_list_file):
        print(f"{url_list_file} already exists. Skipping crawling.")
    else:
        start_url = input("Enter the URL to start crawling: ")
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))

        print(f"Starting crawling at {start_url}")
        crawl(start_url, base_url)
        print("Crawling complete.")

    print("Starting to process URL list for Markdown conversion.")
    process_url_list(url_list_file)
    print("Markdown conversion complete.")

if __name__ == "__main__":
    main()

