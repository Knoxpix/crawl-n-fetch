# crawl-n-fetch
ขั้นตอนที่ 1: การติดตั้งเครื่องมือที่จำเป็น
ติดตั้ง Python และ pip:

ตรวจสอบว่าคุณได้ติดตั้ง Python และ pip แล้ว หากยังไม่ติดตั้งสามารถดาวน์โหลดและติดตั้งได้จาก python.org.

สร้าง Virtual environment

````bash
pip install virtualenv
python3 -m venv venv
source venv/bin/activate
````

ติดตั้งเครื่องมือที่จำเป็น:

ติดตั้ง requests, beautifulsoup4 tqdm และ markdownify โดยใช้ pip:

````bash
pip install requests beautifulsoup4 tqdm markdownify
````
