from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time

# Path ke ChromeDriver
service = Service('chromedriver/win64-126.0.6478.182/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = 'http://repository.untar.ac.id/view/divisions/mana/2022.html'
# url = 'http://repository.unpas.ac.id/view/subjects/A.html'
driver.get(url)

# Tunggu beberapa detik agar halaman selesai dimuat
# Wait a few seconds to allow the page to load
time.sleep(5)

# Locate all paragraph elements containing thesis data
paragraphs = driver.find_elements(By.TAG_NAME, 'p')

data = []
for paragraph in paragraphs:
    try:
        # Extract title and link
        title_element = paragraph.find_element(By.TAG_NAME, 'a')
        title = title_element.text.strip()
        link = title_element.get_attribute('href')
    except:
        title = 'Title not found'
        link = ''

    try:
        # Extract authors
        authors = [span.text.strip() for span in paragraph.find_elements(By.CLASS_NAME, 'person_name')]
        author = ', '.join(authors)
    except:
        author = 'Author not found'
    
    data.append({
        'title': title,
        'author': author,
        'link': link
    })

csv_file = 'hasil_scraping.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'author', 'link'])
    writer.writeheader()
    writer.writerows(data)

print(f"Hasil scraping telah disimpan ke {csv_file}")

driver.quit()