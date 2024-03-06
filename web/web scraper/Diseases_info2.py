import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv


session = requests.Session()

def read_from_link(link):

    response = session.get(link, timeout=10)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'lxml')
    active_div = soup.find('div', class_='col-sm-12 illnessPart1')

    if active_div is not None:
        text = active_div.get_text(separator='\n', strip=True)
        print(text)
        return text
    
    else:
        print("Content not found for URL:", link)
        return "Content not found"

def write_to_csv(output_csv_path, rows):

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Link', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def read_links_and_write_content(input_csv_path, output_csv_path):
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        links = [row['Link'] for row in reader]


    with ThreadPoolExecutor(max_workers=10) as executor:

        future_to_url = {executor.submit(read_from_link, link): link for link in links}
        rows = []
        for future in as_completed(future_to_url):
            link = future_to_url[future]
            data = future.result()
            rows.append({'Link': link, 'information': data})


    write_to_csv(output_csv_path, rows)


input_csv_path = 'C:/Users/siddh/OneDrive/Desktop/C C++/links.csv'
output_csv_path = 'C:/Users/siddh/OneDrive/Desktop/C C++/information2.csv'


read_links_and_write_content(input_csv_path, output_csv_path)
