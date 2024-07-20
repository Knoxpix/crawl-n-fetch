# crawl-n-fetch
ขั้นตอนที่ 1: การติดตั้งเครื่องมือที่จำเป็น
ติดตั้ง Python และ pip:

ตรวจสอบว่าคุณได้ติดตั้ง Python และ pip แล้ว หากยังไม่ติดตั้งสามารถดาวน์โหลดและติดตั้งได้จาก python.org.

สร้าง Virtual environment

````bash
pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
````

ติดตั้งเครื่องมือที่จำเป็น:

ติดตั้ง requests, beautifulsoup4 tqdm และ markdownify โดยใช้ pip:

````bash
pip3 install requests beautifulsoup4 tqdm python-dotenv markdownify
````

สร้างไฟล์ .env:
สร้างไฟล์ .env ในไดเรกทอรีเดียวกับสคริปต์ Python ของคุณและเพิ่ม API key จาก https://jina.ai/reader/ ลงในไฟล์นี้

````makefile
JINA_AUTH_TOKEN={Jina Reader API KEY}
````

การใช้งาน:
รันโค้ดเพื่อเริ่มการ crawl เว็บไซต์, บันทึก URL ลงใน list_url.txt, และแปลงเนื้อหาเป็น Markdown:

````bash
python3 script.py
````

ป้อน URL เพื่อเริ่มการ crawl:
ตัวอย่าง: https://example.com

