import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.shl.com/solutions/products/product-catalog/"
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

cards = soup.find_all('div', class_='product-card')

data = []

for card in cards:
    name_tag = card.find('a', class_='product-card-title')
    name = name_tag.text.strip()
    url = name_tag['href']
    info = card.find_all('div', class_='product-card-meta-item')

    remote = 'No'
    adaptive = 'No'
    duration = 'Not Mentioned'
    test_type = 'Not Mentioned'

    for item in info:
        text = item.text.strip()
        if 'Remote' in text:
            remote = 'Yes' if 'Yes' in text else 'No'
        elif 'Adaptive' in text or 'IRT' in text:
            adaptive = 'Yes' if 'Yes' in text else 'No'
        elif 'minutes' in text.lower():
            duration = text
        else:
            test_type = text

    data.append([name, url, remote, adaptive, duration, test_type])

with open('shl_assessments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'URL', 'Remote Testing Support', 'Adaptive/IRT Support', 'Duration', 'Test Type'])
    writer.writerows(data)

print("✅ Scraped & saved to shl_assessments.csv!")
